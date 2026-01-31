from __future__ import annotations

def digest_selection(selection, syntax="PackLib", caller=None):
    if selection is None:
        return "all"
    if isinstance(selection, str):
        return selection
    if isinstance(selection, (list, tuple)):
        return list(selection)
    return selection
