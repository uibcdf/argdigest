"""Axis 1: the argument contract of a function.

ArgDigest has always covered one axis — *given an argument name, is its value valid and
in canonical form?* That is what argument digesters do. This module adds the other one:
*given a function, which arguments may it receive, and which must it receive?*

Without it, function-dependent rules have nowhere to live and end up scattered across
the per-argument digesters, one `if caller == ...` at a time, so the contract of a
function is never written down in one readable place.

A consumer library declares contracts and domains as data. Everything else — discovery,
resolution order, enforcement, diagnostics, introspection — belongs here.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from functools import lru_cache
from fnmatch import fnmatchcase
from typing import Any, Callable, Iterable, Sequence

#: `admits` values with a reserved meaning. Anything else names a domain.
ADMITS_SIGNATURE = "signature"
ADMITS_ANY = "any"


@dataclass(frozen=True)
class Domain:
    """A named, introspectable set of admissible keyword names.

    Five MolSysMT functions accept the same 118 attribute names through ``**kwargs``.
    A domain lets that be declared once and pointed at, instead of copied per function,
    and lets the accepted names be *read* — which is what makes the real signature of an
    open function documentable rather than only enforceable.

    `contains` decides membership. `members` enumerates it when that is possible, which
    enables near-miss suggestions and introspection. Either one is enough; giving both
    keeps membership cheap while still allowing enumeration.
    """

    name: str
    contains: Callable[[str], bool] | None = None
    members: Callable[[], Iterable[str]] | Iterable[str] | None = None
    description: str | None = None

    def __post_init__(self) -> None:
        if self.contains is None and self.members is None:
            raise ValueError(
                f"Domain {self.name!r} needs 'contains', 'members', or both."
            )

    def __contains__(self, keyword: str) -> bool:
        if self.contains is not None:
            return bool(self.contains(keyword))
        return keyword in set(self.known_members())

    def known_members(self) -> tuple[str, ...]:
        """Return the enumerable members, or an empty tuple when not enumerable."""

        if self.members is None:
            return ()
        members = self.members() if callable(self.members) else self.members
        return tuple(str(member) for member in members)


@dataclass(frozen=True)
class FunctionContract:
    """What a function accepts and requires, declared as data.

    Exactly one of `caller` and `caller_pattern` identifies the function or the family
    it applies to. A pattern uses `fnmatch` syntax against the fully qualified caller,
    so a whole family of adapters can share one contract.
    """

    caller: str | None = None
    caller_pattern: str | None = None
    admits: str | Sequence[str] = ADMITS_SIGNATURE
    requires_any_of: str | Sequence[str] | None = None
    mutually_exclusive: Sequence[Sequence[str]] = field(default_factory=tuple)
    co_required: Sequence[Sequence[str]] = field(default_factory=tuple)
    description: str | None = None

    def __post_init__(self) -> None:
        if (self.caller is None) == (self.caller_pattern is None):
            raise ValueError(
                "A FunctionContract needs exactly one of 'caller' or 'caller_pattern'; "
                f"got caller={self.caller!r}, caller_pattern={self.caller_pattern!r}."
            )

    @property
    def key(self) -> str:
        return self.caller if self.caller is not None else self.caller_pattern  # type: ignore[return-value]

    def admits_anything(self) -> bool:
        return self.admits == ADMITS_ANY

    def has_rules_beyond_admission(self) -> bool:
        """Whether anything has to be checked even when no extra keyword was passed."""

        return bool(self.requires_any_of or self.mutually_exclusive or self.co_required)

    def admitted_domains(self) -> tuple[str, ...]:
        """Domain names this contract admits beyond its own signature."""

        if isinstance(self.admits, str):
            if self.admits in (ADMITS_SIGNATURE, ADMITS_ANY):
                return ()
            return (self.admits,)
        return tuple(str(name) for name in self.admits)


@dataclass(frozen=True)
class Violation:
    """One breach of a function's argument contract."""

    kind: str
    message: str
    hint: str = ""
    keyword: str | None = None


@lru_cache(maxsize=None)
def default_contract(caller: str, has_var_keyword: bool) -> FunctionContract:
    """The contract of a function that declared none.

    A closed signature already declares its own domain, so the default is to hold the
    function to it. This is not a new policy: plain Python raises ``TypeError`` for an
    unexpected keyword, and ArgDigest must never end up *more* permissive than the
    language it wraps.

    A function with ``**kwargs`` deliberately opened its door and ArgDigest cannot guess
    what it meant, so the default there is to admit anything until the consumer declares
    a domain.
    """

    return FunctionContract(
        caller=caller,
        admits=ADMITS_ANY if has_var_keyword else ADMITS_SIGNATURE,
    )


class ContractRegistry:
    """Resolves the contract that applies to a caller, most specific first.

    Resolution order is exact caller, then the longest matching pattern, then the
    default. Longest-pattern-wins keeps specificity predictable without asking the
    consumer to declare priorities.
    """

    def __init__(self, contracts: Iterable[FunctionContract] = ()) -> None:
        self._exact: dict[str, FunctionContract] = {}
        self._patterns: list[FunctionContract] = []
        # Resolution runs on every decorated call, and a caller that matches no pattern
        # would otherwise walk the whole pattern list each time. `None` is memoized too:
        # "nothing declared here" is the answer for most callers in a real library.
        self._resolved: dict[str, FunctionContract | None] = {}
        for contract in contracts:
            self.add(contract)

    def add(self, contract: FunctionContract) -> None:
        if contract.caller is not None:
            self._exact[contract.caller] = contract
        else:
            self._patterns.append(contract)
            self._patterns.sort(key=lambda item: len(item.caller_pattern or ""), reverse=True)
        self._resolved.clear()

    def resolve(self, caller: str) -> FunctionContract | None:
        try:
            return self._resolved[caller]
        except KeyError:
            pass
        contract = self._exact.get(caller)
        if contract is None:
            for candidate in self._patterns:
                if fnmatchcase(caller, candidate.caller_pattern or ""):
                    contract = candidate
                    break
        self._resolved[caller] = contract
        return contract

    def declared_callers(self) -> tuple[str, ...]:
        return tuple(self._exact) + tuple(c.caller_pattern or "" for c in self._patterns)


def _suggest(keyword: str, candidates: Iterable[str]) -> str:
    matches = difflib.get_close_matches(keyword, sorted(set(candidates)), n=1, cutoff=0.75)
    if not matches:
        return ""
    return f" Did you mean {matches[0]!r}?"


def check_contract(
    contract: FunctionContract,
    caller: str,
    signature_parameters: Iterable[str],
    extras: Iterable[str],
    domains: dict[str, Domain],
    present: Iterable[str] = (),
) -> list[Violation]:
    """Check one call against a contract and return every violation found.

    `extras` are the keywords the caller passed that the signature does not declare.
    `present` is every keyword the caller actually supplied, used for the requirement
    and consistency rules. Nothing is raised here: emitting is the caller's decision,
    because the policy that decides between error and warning lives with the plan.
    """

    violations: list[Violation] = []
    signature_parameters = set(signature_parameters)
    extras = list(extras)
    present = set(present)

    admitted_domains = [domains[name] for name in contract.admitted_domains() if name in domains]
    missing_domains = [name for name in contract.admitted_domains() if name not in domains]
    for name in missing_domains:
        violations.append(Violation(
            kind="unknown_domain",
            message=(f"Function contract for {caller!r} admits domain {name!r}, "
                     "which is not registered."),
            hint="Declare the domain in the consumer's domain source, or fix the name.",
        ))

    if not contract.admits_anything():
        vocabulary: list[str] | None = None
        for keyword in extras:
            if any(keyword in domain for domain in admitted_domains):
                continue
            # The vocabulary can run to hundreds of names, and it is needed only to
            # suggest a near miss. Building it eagerly would charge every correct call
            # for a hint that only a wrong one ever reads.
            if vocabulary is None:
                vocabulary = sorted(signature_parameters)
                for domain in admitted_domains:
                    vocabulary.extend(domain.known_members())
            violations.append(Violation(
                kind="unknown_argument",
                keyword=keyword,
                message=f"{caller!r} does not accept the argument {keyword!r}.",
                hint=_suggest(keyword, vocabulary).strip() or
                     "Check the function signature for the accepted arguments.",
            ))

    if contract.requires_any_of is not None:
        required = ([contract.requires_any_of]
                    if isinstance(contract.requires_any_of, str)
                    else list(contract.requires_any_of))
        satisfied = False
        for name in required:
            domain = domains.get(name)
            if domain is not None:
                if any(keyword in domain for keyword in present):
                    satisfied = True
                    break
            elif name in present:
                satisfied = True
                break
        if not satisfied:
            wanted = ", ".join(required)
            violations.append(Violation(
                kind="missing_argument",
                message=(f"{caller!r} needs at least one argument from: {wanted}."),
                hint="The call carries no such argument, so it cannot mean anything.",
            ))

    for group in contract.mutually_exclusive:
        given = [name for name in group if name in present]
        if len(given) > 1:
            violations.append(Violation(
                kind="mutually_exclusive",
                message=(f"{caller!r} accepts only one of {', '.join(group)}; "
                         f"got {', '.join(given)}."),
                hint="Pass exactly one of them.",
            ))

    for group in contract.co_required:
        given = [name for name in group if name in present]
        if given and len(given) != len(group):
            missing = [name for name in group if name not in present]
            violations.append(Violation(
                kind="co_required",
                message=(f"{caller!r} needs {', '.join(group)} together; "
                         f"{', '.join(missing)} missing."),
                hint="These arguments only mean something as a group.",
            ))

    return violations


def describe_contract(contract: FunctionContract, domains: dict[str, Domain]) -> dict[str, Any]:
    """Render a contract as plain data, for documentation and introspection.

    This is why a contract is declarative rather than an opaque callable: the accepted
    domain of a function with ``**kwargs`` is invisible to ``inspect.signature``, and
    this is what makes it readable again.
    """

    described_domains = []
    for name in contract.admitted_domains():
        domain = domains.get(name)
        described_domains.append({
            "name": name,
            "registered": domain is not None,
            "description": None if domain is None else domain.description,
            "members": () if domain is None else domain.known_members(),
        })

    return {
        "caller": contract.caller,
        "caller_pattern": contract.caller_pattern,
        "admits": contract.admits,
        "admitted_domains": described_domains,
        "requires_any_of": contract.requires_any_of,
        "mutually_exclusive": [list(group) for group in contract.mutually_exclusive],
        "co_required": [list(group) for group in contract.co_required],
        "description": contract.description,
    }
