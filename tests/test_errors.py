import pytest
from argdigest import arg_digest, DigestNotDigestedError

def test_rich_error_message():
    @arg_digest(digestion_style="decorator", strictness="error")
    def my_func(my_arg):
        return my_arg

    with pytest.raises(DigestNotDigestedError) as excinfo:
        my_func("invalid_value")

    msg = str(excinfo.value)
    print(f"\nCaught error message:\n{msg}")

    assert "No digester for my_arg" in msg
    # Catalog-backed messages include actionable hints and docs links.
    assert "Docs:" in msg
