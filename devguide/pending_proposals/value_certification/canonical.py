"""Certifying that a value has already been digested, without wrapping it.

The expensive digesters are the ones that *convert*: a unit conversion, a `np.asarray`
over a large frame, an assessment of which form an object is in. Measured on a
5000-atom frame, one such coercion costs 1.67 ms, some seventy times the whole of the
decorator's own per-call machinery. Doing that once is necessary. Doing it again on a
value that has not changed is waste.

The obvious mechanism is to hand the digester's result back inside a box that says "this
is done". ArgDigest tried that, and the box is the problem: it changes the value's
**type**, so every function body downstream has to know about it, and it has to be
unwrapped before the body runs -- which means it stops travelling at the first body it
meets. A value that passes through five nested calls is re-digested four times.

So the claim is attached to the value's **identity** instead. `certify` returns the very
same object; what changes is that ArgDigest now knows something about it. The value
travels as itself, through however many bodies, and every call in the chain can skip the
work.

Two properties make that safe rather than merely fast:

**A claim names the verification it represents.** Not "this value is fine" but "this
value satisfies *this digester*". A claim issued by one library's digester cannot
silence another library's digester for the same argument name -- which the wrapper it
replaces could, and did.

**Modification costs the passport.** A certified array is frozen, so mutating it
requires an explicit `flags.writeable = True`, and that act is observable. Once observed,
the claim is dropped permanently rather than merely reported missing, so refreezing does
not bring it back.
"""

from __future__ import annotations

import sys
import threading
import weakref
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

#: How strongly a claim is guarded against the value changing underneath it.
#:
#: `form` is the default and the right answer for almost every digester, because almost
#: every digester guarantees *form*: this is nm, float64, (n, 3). Rotating those
#: coordinates in place does not make that false, and MolSysMT rotates coordinates in
#: place in `structure/rotate.py` and `structure/align_principal_axes.py`. A guard that
#: froze them would turn correct scientific code into a `ValueError`.
#:
#: `frozen` is for the rarer digester whose guarantee dies if any value changes -- "no
#: NaN", "inside the box", "indices sorted". Freezing is the only cheap way to notice
#: that, because a content change leaves no trace in shape or dtype. It is opt-in
#: because it is intrusive: the array becomes read-only for everyone.
GUARD_FORM = "form"          #: shape and dtype are checked; values may change freely
GUARD_FROZEN = "frozen"      #: read-only; unfreezing is observable and revokes the claim
GUARD_IDENTITY = "identity"  #: not an array; the claim rests on object identity alone

#: `source` omitted, which is not the same as `source=None`. One is a question the
#: digester has not answered; the other is the answer "there was no input".
_UNSET = object()


def _name(fn: Callable[..., Any]) -> str:
    return getattr(fn, "__qualname__", None) or repr(fn)


@dataclass(frozen=True, slots=True)
class Claim:
    """What was verified about one value, and by which digester.

    `by` is the identity of the verification, and it is what a claim is *for*: the
    decorator skips a digester only when the claim it finds was issued by that same
    digester. Anything weaker would let a claim silence a check it never performed.
    """

    by: Callable[..., Any]
    attributes: Mapping[str, Any] = field(default_factory=dict)
    guard: str = GUARD_IDENTITY
    shape: tuple[int, ...] | None = None
    dtype: Any | None = None
    issued_by: str | None = None

    def describe(self) -> dict[str, Any]:
        """Render the claim as plain data, for introspection and diagnostics."""

        return {
            "by": getattr(self.by, "__qualname__", repr(self.by)),
            "by_module": getattr(self.by, "__module__", None),
            "attributes": dict(self.attributes),
            "guard": self.guard,
            "shape": self.shape,
            "dtype": None if self.dtype is None else str(self.dtype),
            "issued_by": self.issued_by,
        }


class _Registry:
    """Claims held weakly, keyed by the identity of the value they describe.

    `id()` alone would be unsound: an address is reused once the object dies, and a new
    value could inherit the claim of a dead one. Holding a weak reference alongside it,
    with a callback that drops the entry, closes that -- the claim cannot outlive the
    object it describes.
    """

    def __init__(self) -> None:
        self._claims: dict[int, Claim] = {}
        self._refs: dict[int, weakref.ref] = {}
        self._lock = threading.RLock()

    def add(self, value: Any, claim: Claim) -> bool:
        key = id(value)

        def _drop(_reference: Any, key: int = key) -> None:
            with self._lock:
                self._claims.pop(key, None)
                self._refs.pop(key, None)

        try:
            reference = weakref.ref(value, _drop)
        except TypeError:
            # int, str, tuple and friends cannot be weakly referenced. They are also
            # cheap to digest, so the mechanism simply does not apply to them.
            return False
        with self._lock:
            self._refs[key] = reference
            self._claims[key] = claim
        return True

    def get(self, value: Any) -> Claim | None:
        return self._claims.get(id(value))

    def drop(self, value: Any) -> bool:
        key = id(value)
        with self._lock:
            self._refs.pop(key, None)
            return self._claims.pop(key, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._claims.clear()
            self._refs.clear()

    def __len__(self) -> int:
        return len(self._claims)


_REGISTRY = _Registry()


def _is_ndarray(value: Any) -> bool:
    """Whether this is a numpy array, without importing numpy to find out.

    A consumer that never touches numpy should not pay an import for a check that will
    always be false for it. If numpy is not already loaded, nothing here can be one.
    """

    numpy = sys.modules.get("numpy")
    return numpy is not None and isinstance(value, numpy.ndarray)


def certify(value: Any, *, by: Callable[..., Any], guard: str = GUARD_FORM,
            source: Any = _UNSET, issued_by: str | None = None,
            **attributes: Any) -> Any:
    """Record that `value` satisfies the verification `by`, and return it unchanged.

    `by` is required. A claim that does not name what it represents is the defect this
    mechanism exists to avoid: it would let any digester's result silence any other
    digester for the same argument name.

    `guard` says what has to stay true for the claim to keep holding, and the default
    leaves the value untouched. See the module constants: `form` for a guarantee about
    shape and dtype, which is what almost every digester makes; `frozen` for one that
    dies if any value changes.

    `source` is the raw input the digester received, and it answers one question: did
    this digester *produce* `value`, or hand back what it was given? `np.asarray` returns
    the very same object when no conversion is needed, so a digester frequently returns
    its own input. It only matters under `guard="frozen"`, where certifying would freeze
    an array the caller still owns and turn their next write into a `ValueError` inside
    their own code -- so it is **required** there, and optional otherwise. Pass the
    digester's input, or `source=None` when the value was built from nothing.
    """

    is_array = _is_ndarray(value)
    freezing = guard == GUARD_FROZEN and is_array

    if freezing and source is _UNSET:
        raise TypeError(
            f"certify(guard='frozen') needs 'source' for the array certified by "
            f"{_name(by)}. Freezing one the digester did not produce takes an array the "
            "caller still owns, and their next write would raise inside their own code. "
            "Pass the digester's input as source=, or source=None if the array was built "
            "from nothing."
        )

    if source is not _UNSET and source is not None and value is source and freezing:
        # Nothing was produced: the input came back untouched, so it is not ours to
        # freeze. Under the other guards there is nothing to seize, so this does not
        # apply and the claim is recorded normally.
        return value

    shape = None
    dtype = None
    if is_array:
        shape = value.shape
        dtype = value.dtype
        if freezing:
            value.setflags(write=False)
    else:
        guard = GUARD_IDENTITY

    _REGISTRY.add(value, Claim(by=by, attributes=dict(attributes), guard=guard,
                               shape=shape, dtype=dtype, issued_by=issued_by))
    return value


def claim_for(value: Any, *, by: Callable[..., Any] | None = None) -> Claim | None:
    """The claim held for `value`, or None.

    When `by` is given, the claim is returned only if it was issued by that exact
    verification. This is the decorator's question -- *may I skip this digester?* -- and
    the answer is no unless the claim is the one that digester would have produced.

    A frozen claim is checked before it is honoured. Finding the value writeable again,
    or reshaped, means it was modified since, so the claim is **revoked** rather than
    merely withheld: refreezing must not resurrect a guarantee that no longer holds.
    """

    claim = _REGISTRY.get(value)
    if claim is None:
        return None

    # Structural change revokes under either array guard: reshaping or retyping a value
    # makes any claim about it false. Only `frozen` additionally reads the writeable
    # flag, because only a content guarantee can be broken by a write that leaves shape
    # and dtype alone.
    if claim.guard in (GUARD_FORM, GUARD_FROZEN) and (
            value.shape != claim.shape
            or value.dtype != claim.dtype
            or (claim.guard == GUARD_FROZEN and value.flags.writeable)):
        _REGISTRY.drop(value)
        return None

    if by is not None and claim.by is not by:
        return None
    return claim


def revoke(value: Any) -> bool:
    """Drop any claim held for `value`. Returns whether there was one."""

    return _REGISTRY.drop(value)


def clear_claims() -> None:
    """Drop every claim. For tests, and for a consumer resetting between runs."""

    _REGISTRY.clear()


def claim_count() -> int:
    """How many claims are currently held. For diagnostics and leak checks."""

    return len(_REGISTRY)
