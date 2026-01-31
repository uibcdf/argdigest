class DigestError(Exception):
    """Base exception for ArgDigest errors."""

    def __init__(self, message: str, context=None, hint: str | None = None):
        super().__init__(message)
        self.context = context
        self.hint = hint

    def __str__(self):
        msg = super().__str__()
        details = []
        if self.context:
            if hasattr(self.context, "function_name"):
                details.append(f"Function: {self.context.function_name}")
            if hasattr(self.context, "argname"):
                details.append(f"Argument: {self.context.argname}")
            if hasattr(self.context, "value"):
                # Avoid printing massive objects
                val_repr = repr(self.context.value)
                if len(val_repr) > 50:
                    val_repr = val_repr[:47] + "..."
                details.append(f"Value: {val_repr}")
        
        if self.hint:
            details.append(f"Hint: {self.hint}")
        
        if details:
            return f"{msg}\n  " + "\n  ".join(details)
        return msg


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
