import pytest
from argdigest import arg_digest, argument_digest, DigestNotDigestedError

def test_rich_error_message():
    @arg_digest(digestion_style="decorator", strictness="error")
    def my_func(my_arg):
        return my_arg

    with pytest.raises(DigestNotDigestedError) as excinfo:
        my_func("invalid_value")

    msg = str(excinfo.value)
    print(f"\nCaught error message:\n{msg}")

    assert "Argument 'my_arg' from 'my_func' failed." in msg
    assert "No digester for my_arg" in msg