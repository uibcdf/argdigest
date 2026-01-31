from typing import Any, Iterable
from ..core.registry import register_pipeline

# --- Boolean Coercers ---

@register_pipeline(kind="std", name="to_bool")
def to_bool(value: Any, ctx: Any = None) -> bool:
    """
    Converts value to boolean.
    Handles strings: 'true', '1', 'yes', 'on' are True.
    """
    if isinstance(value, str):
        val_lower = value.strip().lower()
        if val_lower in ("true", "1", "yes", "on", "t", "y"):
            return True
        if val_lower in ("false", "0", "no", "off", "f", "n"):
            return False
    return bool(value)

# --- Collection Coercers ---

@register_pipeline(kind="std", name="to_list")
def to_list(value: Any, ctx: Any = None) -> list[Any]:
    """
    Ensures value is a list.
    If it's a scalar (including string), wraps it: [value].
    If it's a tuple or other iterable (excluding str), converts to list.
    """
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)): # specific types usually wanted
        return list(value)
    # Check general iterable but exclude known scalars? 
    # For simplicity/safety in science context where numpy arrays exist:
    import collections.abc
    if isinstance(value, collections.abc.Iterable):
        return list(value)
    return [value]

@register_pipeline(kind="std", name="to_tuple")
def to_tuple(value: Any, ctx: Any = None) -> tuple[Any, ...]:
    """Ensures value is a tuple."""
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(value)
    import collections.abc
    if isinstance(value, collections.abc.Iterable):
        return tuple(value)
    return (value,)

# --- String Coercers ---

@register_pipeline(kind="std", name="strip")
def strip(value: Any, ctx: Any = None) -> Any:
    """Strips whitespace if value is a string."""
    if isinstance(value, str):
        return value.strip()
    return value

@register_pipeline(kind="std", name="lower")
def lower(value: Any, ctx: Any = None) -> Any:
    """Converts to lowercase if value is a string."""
    if isinstance(value, str):
        return value.lower()
    return value

@register_pipeline(kind="std", name="upper")
def upper(value: Any, ctx: Any = None) -> Any:
    """Converts to uppercase if value is a string."""
    if isinstance(value, str):
        return value.upper()
    return value
