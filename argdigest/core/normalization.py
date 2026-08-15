"""Declared normalization: argument-name aliases as data.

Renaming an argument before it is judged is what lets a library accept the names its
users actually type — `residue_index` for `group_index` — without every downstream layer
having to know about it. ArgDigest has always supported this through the `standardizer`
hook, one callable per library, which in practice grows into a chain of
`if caller == ...` branches.

That is the shape the function contract removed for admission rules, and this module
removes it for renaming: aliases are declared as data, discovered like digesters and
contracts, and composed by ArgDigest.

Rules are deliberately **static**. An earlier design generated target names from a
template such as `{element}_{name}`, which is shorter to write and admits names that do
not exist: on the reference consumer it would have produced six attributes nobody
defines. A table declares only what is real.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from fnmatch import fnmatchcase
from typing import Any

from .context import Context
from .errors import ArgumentConsistencyError

#: Applied to every caller.
APPLIES_TO_ALL = "*"


@dataclass(frozen=True)
class AliasTable:
    """A set of argument-name aliases, optionally scoped to callers and to a context.

    `applies_to` is an exact caller, an `fnmatch` pattern, or `"*"` for every caller.

    `when` guards the table on the value of another argument of the same call, which is
    what covers a name whose meaning depends on context: `name` means `atom_name` when
    `element="atom"`. It is an equality test against already-bound arguments, not an
    expression language.
    """

    aliases: Mapping[str, str]
    applies_to: str = APPLIES_TO_ALL
    when: Mapping[str, Any] | None = None
    description: str | None = None

    def __post_init__(self) -> None:
        if not self.aliases:
            raise ValueError("An AliasTable needs at least one alias.")
        for source, target in self.aliases.items():
            if source == target:
                raise ValueError(
                    f"Alias {source!r} maps to itself, which cannot be what was meant."
                )

    @property
    def specificity(self) -> tuple[int, int]:
        """Rank for resolution: an exact caller beats a longer pattern beats `*`."""

        if self.applies_to == APPLIES_TO_ALL:
            return (0, 0)
        if any(character in self.applies_to for character in "*?["):
            return (1, len(self.applies_to))
        return (2, len(self.applies_to))

    def matches_caller(self, caller: str) -> bool:
        if self.applies_to == APPLIES_TO_ALL:
            return True
        return fnmatchcase(caller, self.applies_to)

    def matches_context(self, bound: Mapping[str, Any]) -> bool:
        if not self.when:
            return True
        return all(bound.get(name) == value for name, value in self.when.items())


class NormalizationRegistry:
    """Resolves which alias tables apply to a caller, most specific first."""

    def __init__(self, tables: Iterable[AliasTable] = ()) -> None:
        self._tables: list[AliasTable] = []
        # Which tables match a caller depends only on the caller, so it is cached; the
        # `when` guard still has to be evaluated per call, because it reads values.
        self._by_caller: dict[str, tuple[AliasTable, ...]] = {}
        for table in tables:
            self.add(table)

    def add(self, table: AliasTable) -> None:
        self._tables.append(table)
        self._tables.sort(key=lambda item: item.specificity, reverse=True)
        self._by_caller.clear()

    def for_caller(self, caller: str) -> tuple[AliasTable, ...]:
        try:
            return self._by_caller[caller]
        except KeyError:
            pass
        matching = tuple(table for table in self._tables if table.matches_caller(caller))
        self._by_caller[caller] = matching
        return matching

    def tables(self) -> tuple[AliasTable, ...]:
        return tuple(self._tables)

    def __bool__(self) -> bool:
        return bool(self._tables)


def apply_normalization(registry: NormalizationRegistry, caller: str,
                        bound: dict[str, Any],
                        supplied: set[str] | None = None) -> dict[str, Any]:
    """Rename the arguments of one call according to the declared tables.

    Tables are applied most specific first, so a caller-scoped alias wins over a global
    one for the same name. A name already renamed is not reconsidered: renaming is a
    single pass, never a chain.

    Insertion order is preserved, because a caller reading a traceback or a repr should
    see arguments in the order they were written.

    `supplied` names the arguments the caller actually wrote. Collision detection needs
    it: `bound` has defaults applied, so without it a canonical name resting on its
    default looks exactly like one the caller passed, and every alias whose target has a
    default would be rejected as a duplicate. Omitting it keeps the older, defaults-blind
    behaviour.
    """

    tables = registry.for_caller(caller)
    if not tables:
        return bound

    renames: dict[str, str] = {}
    for table in tables:
        if not table.matches_context(bound):
            continue
        for source, target in table.aliases.items():
            if source in bound and source not in renames:
                renames[source] = target
    if not renames:
        return bound

    # Two names are alternatives only if the caller wrote both. A name present merely
    # because `apply_defaults` put it there was never a choice the caller made.
    contested = bound if supplied is None else [n for n in bound if n in supplied]
    sources_by_target: dict[str, list[str]] = {}
    for source in contested:
        target = renames.get(source, source)
        sources_by_target.setdefault(target, []).append(source)

    conflicts = {
        target: sources
        for target, sources in sources_by_target.items()
        if len(sources) > 1
    }
    if conflicts:
        details = "; ".join(
            f"{target!r} from {', '.join(repr(source) for source in sources)}"
            for target, sources in conflicts.items()
        )
        conflicting_values = {
            target: {source: bound[source] for source in sources}
            for target, sources in conflicts.items()
        }
        raise ArgumentConsistencyError(
            f"Call to {caller!r} supplies more than one name for the same argument: "
            f"{details}. Aliases and canonical names are alternatives.",
            context=Context(
                function_name=caller,
                argname=", ".join(conflicts),
                value=conflicting_values,
                all_args=bound,
            ),
            hint="Pass exactly one of the conflicting names.",
        )

    if supplied is None:
        return {renames.get(name, name): value for name, value in bound.items()}

    # A canonical name that is present only because defaults were applied is superseded
    # by the alias the caller did write. Without this it would depend on dict order
    # which of the two survived, and the default would overwrite the supplied value
    # whenever the canonical name is declared later in the signature.
    superseded = {
        renames[source]
        for source in renames
        if source in supplied and renames[source] not in supplied
    }
    result: dict[str, Any] = {}
    for name, value in bound.items():
        if name in superseded and name not in renames:
            continue
        result[renames.get(name, name)] = value
    return result


def describe_normalization(registry: NormalizationRegistry,
                           caller: str | None = None) -> list[dict[str, Any]]:
    """Render the declared aliases as plain data, optionally for one caller.

    Declaring rules as data rather than as a callable is what makes this possible: the
    alternative names a function accepts can be listed in its documentation instead of
    living undocumented inside a branch of a standardizer.
    """

    tables = registry.tables() if caller is None else registry.for_caller(caller)
    return [
        {
            "applies_to": table.applies_to,
            "when": dict(table.when) if table.when else None,
            "aliases": dict(table.aliases),
            "description": table.description,
        }
        for table in tables
    ]
