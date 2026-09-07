import pytest

from argdigest import DigestNotDigestedError, arg_digest


def test_rich_error_message():
    @arg_digest(digestion_style="decorator", strictness="error")
    def my_func(my_arg):
        return my_arg

    with pytest.raises(DigestNotDigestedError) as excinfo:
        my_func("invalid_value")

    msg = str(excinfo.value)
    print(f"\nCaught error message:\n{msg}")

    # The catalog frames the sentence; the raise site contributes the fact.
    assert "Argument 'my_arg' of" in msg
    assert "No digester for 'my_arg'." in msg
    # A catalog-backed message carries an actionable hint and a link.
    assert "Please report it at" in msg
