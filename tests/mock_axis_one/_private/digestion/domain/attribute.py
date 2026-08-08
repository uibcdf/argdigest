from argdigest import Domain

ATTRIBUTES = ("n_atoms", "n_bonds", "coordinates")

domain = Domain(name="attribute", contains=lambda keyword: keyword in ATTRIBUTES,
                members=lambda: ATTRIBUTES,
                description="canonical attribute names")
