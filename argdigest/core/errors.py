class DigestError(Exception):
    """Base exception for ArgDigest errors."""

    def __init__(self, message: str, context=None, hint: str | None = None):
        super().__init__(message)
        self.context = context
        self.hint = hint


class DigestTypeError(DigestError):
    """Raised when an argument has an unexpected type."""


class DigestValueError(DigestError):
    """Raised when an argument has an invalid value."""


class DigestInvariantError(DigestError):
    """Raised when a semantic/invariant rule is violated."""


class DigestNotDigestedError(DigestError):
    """Raised when an argument has no associated digester."""


class DigestNotDigestedWarning(Warning):
    """Warning emitted when an argument has no associated digester."""
