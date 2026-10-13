"""Public declaration-only diagnostics and explicit application bootstrap."""

from inspect import signature

from smonitor import integrations

from ._private.smonitor import PACKAGE_ROOT


def _registration_only_available():
    return callable(getattr(integrations, "register_provider", None)) and (
        "bootstrap_policy" in signature(integrations.DiagnosticBundle).parameters
    )


def register_diagnostics():
    """Register ArgDigest catalogs without applying application diagnostics policy.

    Requires SMonitor's declaration-only DiagnosticBundle capability. Older
    providers retain their original import/bootstrap behavior and refuse this
    explicit capability request. Registration returns the provider's public
    declaration receipt and does not activate logging or warning hooks.
    """
    if not _registration_only_available():
        raise RuntimeError(
            "Registration-only diagnostics requires SMonitor's public "
            "DiagnosticBundle(bootstrap_policy=False) capability."
        )
    return integrations.register_provider(PACKAGE_ROOT)


def configure_diagnostics(*, use_provider_policy=False):
    """Explicitly bootstrap diagnostics, preserving an existing application policy.

    Set use_provider_policy=True only when the application deliberately chooses
    ArgDigest's recommendations over its existing policy. That explicit override
    requires SMonitor's application-policy-preserving configuration capability.
    """
    if type(use_provider_policy) is not bool:
        raise TypeError("use_provider_policy must be a boolean")
    if use_provider_policy:
        if (
            "use_provider_policy"
            not in signature(integrations.ensure_configured).parameters
        ):
            raise RuntimeError(
                "This SMonitor provider cannot explicitly override policy"
            )
        integrations.ensure_configured(PACKAGE_ROOT, use_provider_policy=True)
    else:
        integrations.ensure_configured(PACKAGE_ROOT)


def _initialize_diagnostics():
    if _registration_only_available():
        register_diagnostics()
    else:
        # Preserve the delivered contract on the existing supported provider floor.
        configure_diagnostics()
