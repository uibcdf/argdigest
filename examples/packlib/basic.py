"""Example functions using package-style argument digesters."""

from argdigest import digest


@digest(config="packlib._argdigest")
def get(item, selection=None, syntax="PackLib", skip_digestion=False, **kwargs):
    return item, selection, syntax
