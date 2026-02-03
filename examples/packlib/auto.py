"""Example using auto config discovery via packlib/_argdigest.py."""

from argdigest import arg_digest


@arg_digest()
def get_auto(item, selection=None, syntax="PackLib", skip_digestion=False):
    return item, selection, syntax
