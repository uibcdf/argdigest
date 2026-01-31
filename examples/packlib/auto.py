"""Example using auto config discovery via packlib/_argdigest.py."""

from argdigest import digest


@digest()
def get_auto(item, selection=None, syntax="PackLib", skip_digestion=False):
    return item, selection, syntax
