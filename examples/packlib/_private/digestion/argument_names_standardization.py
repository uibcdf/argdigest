def argument_names_standardization(caller, kwargs):
    if "name" in kwargs:
        kwargs = dict(kwargs)
        kwargs["item_name"] = kwargs.pop("name")
    return kwargs
