# A consumer that declares both axes, used to exercise the real discovery path rather
# than injecting registries into a decorated function's closure.

DIGESTION_SOURCE = "tests.mock_axis_one._private.digestion.argument"
DIGESTION_STYLE = "package"
STRICTNESS = "ignore"

FUNCTION_SOURCE = "tests.mock_axis_one._private.digestion.function"
DOMAIN_SOURCE = "tests.mock_axis_one._private.digestion.domain"
UNKNOWN_ARGUMENT = "error"

NORMALIZATION_SOURCE = "tests.mock_axis_one._private.digestion.normalization"
