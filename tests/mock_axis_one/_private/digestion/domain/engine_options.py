from argdigest import Domain

# A delegating domain: which options are admissible depends on the engine chosen for the
# call. The table is data, so it can be read back and documented.
domain = Domain(
    name='engine_options',
    depends_on='engine',
    by_value={
        'MolSysMT': ('threshold', 'parallel'),
        'OpenMM': ('threshold', 'platform'),
    },
    description='options accepted by each computation engine',
)
