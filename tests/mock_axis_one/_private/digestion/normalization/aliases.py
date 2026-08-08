from argdigest import AliasTable

TABLES = [
    # Global: the name users type for a canonical one.
    AliasTable(aliases={"n_atomz": "n_atoms", "coords": "coordinates"},
               description="common misspellings kept as aliases"),

    # Caller-scoped: only this function renames it.
    AliasTable(applies_to="tests.mock_axis_one.api.get",
               aliases={"attr": "n_bonds"}),

    # Context-guarded: the same name means different things depending on `element`.
    AliasTable(applies_to="tests.mock_axis_one.api.get", when={"element": "atom"},
               aliases={"name": "n_atoms"}),
    AliasTable(applies_to="tests.mock_axis_one.api.get", when={"element": "bond"},
               aliases={"name": "n_bonds"}),
]
