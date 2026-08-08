from argdigest import FunctionContract

CONTRACTS = [
    FunctionContract(caller="tests.mock_axis_one.api.get", admits="attribute"),
    FunctionContract(caller="tests.mock_axis_one.api.measure", admits="attribute",
                     requires_any_of="attribute"),
    FunctionContract(caller_pattern="tests.mock_axis_one.api.to_file_*",
                     admits="signature"),
    FunctionContract(caller="tests.mock_axis_one.api.pick",
                     mutually_exclusive=[("by_name", "by_index")]),
]
