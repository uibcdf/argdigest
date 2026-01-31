import pytest
from argdigest import digest, DigestNotDigestedError

def test_rich_error_message():
    @digest(digestion_style="decorator", strictness="error")
    def my_func(my_arg):
        return my_arg

    with pytest.raises(DigestNotDigestedError) as excinfo:
        my_func("invalid_value")
    
    msg = str(excinfo.value)
    print(f"\nCaught error message:\n{msg}")

    assert "Argument 'my_arg' from" in msg
    assert "Function: tests.test_errors.my_func" in msg or "Function: test_errors.my_func" in msg
    assert "Argument: my_arg" in msg
    assert "Value: 'invalid_value'" in msg
    assert "Hint: Check if the argument name is correct" in msg
