import pytest
try:
    import pyunitwizard as puw
    from argdigest.contrib import pyunitwizard_support as puw_support
    HAS_PUW = True
except ImportError:
    HAS_PUW = False

from argdigest import arg_digest, DigestValueError

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_integration_check_and_standardize():
    try:
        puw.configure.load_library(['pint'])
        puw.configure.set_default_form('pint')
        puw.configure.set_standard_units(['nm', 'ps'])
    except Exception:
        pass

    @arg_digest.map(
        dist={
            "kind": "quantity",
            "rules": [
                puw_support.is_quantity(),
                puw_support.check(dimensionality={'[L]': 1}),
                puw_support.standardize()
            ]
        }
    )
    def set_distance(dist):
        return dist

    q = puw.quantity(1.0, "nm")
    res = set_distance(q)
    assert puw.are_equal(res, q)

    q_time = puw.quantity(1.0, "ps")
    with pytest.raises(DigestValueError, match="Physical validation failed"):
        set_distance(q_time)

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_conversion():
    @arg_digest.map(
        time={
            "kind": "time",
            "rules": [
                puw_support.convert(to_unit="ps")
            ]
        }
    )
    def process_time(time):
        return time

    q_ns = puw.quantity(1.0, "ns") 
    res = process_time(q_ns)
    val = puw.get_value(res)
    assert val == pytest.approx(1000.0)

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_context_decorator():
    q = puw.quantity(1.0, "ns")
    puw.configure.set_standard_units(['nm', 'ps'])

    @arg_digest.map(val={"kind": "q", "rules": [puw_support.standardize()]})
    def default_std(val):
        return val

    res1 = default_std(q)
    assert "picosecond" in str(puw.get_unit(res1))

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_conversion_error():
    @arg_digest.map(val={"kind": "q", "rules": [puw_support.convert(to_unit="invalid_unit")]})
    def f(val): return val

    q = puw.quantity(1.0, "nm")
    with pytest.raises(DigestValueError, match="Conversion to invalid_unit failed"):
        f(q)