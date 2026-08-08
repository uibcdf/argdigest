"""A minimal public surface covering every shape axis 1 has to handle."""

from argdigest import arg_digest

CONFIG = "tests.mock_axis_one._argdigest"


@arg_digest(config=CONFIG)
def extract(molsys, selection="all", structure_indices="all", skip_digestion=False):
    """Closed signature: protected by the default, declares nothing."""
    return structure_indices


@arg_digest(config=CONFIG)
def get(molsys, element="atom", skip_digestion=False, **kwargs):
    """Open signature with a declared domain."""
    return sorted(kwargs)


@arg_digest(config=CONFIG)
def measure(molsys, skip_digestion=False, **kwargs):
    """Open signature that requires at least one member of its domain."""
    return sorted(kwargs)


@arg_digest(config=CONFIG)
def to_file_pdb(molsys, path=None, skip_digestion=False):
    """Matched by a family pattern rather than an exact caller."""
    return path


@arg_digest(config=CONFIG)
def pick(molsys, by_name=None, by_index=None, skip_digestion=False):
    """Two arguments that may not travel together."""
    return by_name if by_name is not None else by_index


@arg_digest(config=CONFIG)
def wide_open(molsys, skip_digestion=False, **kwargs):
    """Open signature with no declared domain: admits anything, by design."""
    return sorted(kwargs)


@arg_digest(config=CONFIG)
def compute(molsys, engine="MolSysMT", skip_digestion=False, **kwargs):
    """Open signature whose admissible keywords depend on the engine."""
    return sorted(kwargs)
