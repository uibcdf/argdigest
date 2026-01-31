import pytest
from argdigest import digest
try:
    import pyunitwizard as puw
    from argdigest.contrib import pyunitwizard_support as puw_support
    HAS_PUW = True
except ImportError:
    HAS_PUW = False

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_integration_check_and_standardize():
    
    # Configure PUW for the test (mocking standard behavior)
    # Assuming openmm.unit or pint is available. Let's use pint via string form if possible.
    try:
        puw.configure.load_library(['pint'])
        puw.configure.set_default_form('pint')
        puw.configure.set_standard_units(['nm', 'ps']) # Define standards!
    except:
        pass # Hope defaults work or libraries are loaded

    @digest.map(
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

    # Create a quantity
    q = puw.quantity(1.0, "nm")
    
    # Pass it
    res = set_distance(q)
    
    # Should be valid and standardized
    assert puw.are_equal(res, q)
    
    # Fail case: wrong dimension (Time instead of Length)
    q_time = puw.quantity(1.0, "ps")
    
    from argdigest import DigestValueError
    with pytest.raises(DigestValueError, match="Physical validation failed"):
        set_distance(q_time)

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_conversion():
    
    @digest.map(
        time={
            "kind": "time",
            "rules": [
                puw_support.convert(to_unit="ps")
            ]
        }
    )
    def process_time(time):
        return time
    
    q_ns = puw.quantity(1.0, "ns") # 1 ns = 1000 ps
    
    res = process_time(q_ns)
    
    val = puw.get_value(res)
    assert val == pytest.approx(1000.0)
