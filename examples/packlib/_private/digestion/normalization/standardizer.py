from .aliases import GLOBAL_ALIASES
from .caller_rules import CALLER_ALIASES
from .dynamic_rules import CALLER_DYNAMIC


def _apply_aliases(kwargs, mapping):
    out = dict(kwargs)
    for old, new in mapping.items():
        if old in out:
            out[new] = out.pop(old)
    return out


def standardizer(caller, kwargs):
    if caller in CALLER_ALIASES:
        kwargs = _apply_aliases(kwargs, CALLER_ALIASES[caller])

    kwargs = _apply_aliases(kwargs, GLOBAL_ALIASES)

    if caller in CALLER_DYNAMIC:
        kwargs = CALLER_DYNAMIC[caller](caller, kwargs)

    return kwargs
