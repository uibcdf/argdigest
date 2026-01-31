
def normalize_get(caller, kwargs):
    if "name" in kwargs and "element" in kwargs:
        kwargs = dict(kwargs)
        kwargs[f"{kwargs['element']}_name"] = kwargs.pop("name")
    return kwargs


CALLER_DYNAMIC = {
    "packlib.basic.get": normalize_get,
}
