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
    except Exception:
        pass # Hope defaults work or libraries are loaded

    print(f"DEBUG TEST: puw={puw}")
    print(f"DEBUG TEST: puw.is_quantity={getattr(puw, 'is_quantity', 'MISSING')}")

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


@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_context_decorator():
    # Setup: define a quantity in ns
    q = puw.quantity(1.0, "ns")
    
    # 1. Function that standardizes to 'pint' default (configured globally as nm/ps in prev test)
    # We rely on previous test config or set it here.
    puw.configure.set_standard_units(['nm', 'ps'])
    
    @digest.map(val={"kind": "q", "rules": [puw_support.standardize()]})
    def default_std(val):
        return val
        
    res1 = default_std(q)
    # Should be ps
    assert str(puw.get_unit(res1)) == "picosecond"
    
    # 2. Function that OVERRIDES context to use 'fs' (femtoseconds)
    @digest.map(
        puw_context={"standard_units": ["nm", "fs"]},
        val={"kind": "q", "rules": [puw_support.standardize()]}
    )
    def fast_std(val):
        return val
        
    res2 = fast_std(q)
    # Should be fs
    assert str(puw.get_unit(res2)) == "femtosecond"
    assert puw.get_value(res2) == pytest.approx(1000000.0) # 1 ns = 1e6 fs

@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_puw_conversion_error():
    from argdigest import DigestValueError
    @digest.map(val={"kind": "q", "rules": [puw_support.convert(to_unit="invalid_unit")]})
    def f(val): return val
    
    q = puw.quantity(1.0, "nm")
    with pytest.raises(DigestValueError, match="Conversion to invalid_unit failed"):
        f(q)
