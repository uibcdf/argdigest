"""Example functions using package-style argument digesters."""

from argdigest import digest


@digest(config="packlib._argdigest", type_check=True)
def get(item, selection=None, syntax="PackLib", skip_digestion=False, **kwargs):
    return item, selection, syntax
