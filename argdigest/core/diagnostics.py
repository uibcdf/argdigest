"""Adapt SMonitor's public capture policy before constructing diagnostics.

Older supported providers retain detailed behavior. Restrictive capture requires
the provider's actual scoped API; ArgDigest never substitutes a global switch.
"""

from contextlib import nullcontext
from typing import Any, Callable

import smonitor


def get_capture_policy():
    getter = getattr(smonitor, "get_capture_policy", None)
    return getter() if getter is not None else None


def detailed_diagnostics() -> bool:
    policy = get_capture_policy()
    return policy is None or (
        policy.arguments and policy.exception_text and policy.extra
    )


def diagnostic_detail(factory: Callable[[], str]) -> str | None:
    """Render optional free text only when the active policy permits it."""
    return factory() if detailed_diagnostics() else None


def resolve_capture_policy(value: Any):
    """Resolve named policies without converting arbitrary policy objects."""
    if value is None:
        return None
    policy_type = getattr(smonitor, "CapturePolicy", None)
    if type(value) is str and value == "detailed":
        return policy_type() if policy_type is not None else None
    if policy_type is None or not hasattr(smonitor, "diagnostic_scope"):
        from .errors import DigestError

        raise DigestError(code="ARG-ERR-CAPTURE-001")
    if type(value) is str and value == "metadata_only":
        return smonitor.METADATA_ONLY
    if type(value) is policy_type:
        return value
    from .errors import DigestValueError

    raise DigestValueError(detail="Unsupported diagnostic capture policy.")


def diagnostic_scope(policy):
    return smonitor.diagnostic_scope(policy) if policy is not None else nullcontext()
