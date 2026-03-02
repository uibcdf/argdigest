from argdigest.core.utils import bind_arguments

def test_bind_extra_kwargs_success_filtering():
    def my_func(a, b):
        return a + b

    # This should now PASS because 'extra' will be filtered out
    bound = bind_arguments(my_func, a=1, b=2, extra=3)
    assert bound['a'] == 1
    assert bound['b'] == 2
    assert 'extra' not in bound

def test_bind_extra_kwargs_success_if_varkw():
    def my_func(a, **kwargs):
        return a

    # This should pass
    bound = bind_arguments(my_func, a=1, extra=3)
    assert bound['a'] == 1
    # bind_arguments flattens **kwargs into the returned dictionary
    assert bound['extra'] == 3
