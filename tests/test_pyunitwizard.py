import numpy as np
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


@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_the_canonical_pipeline_returns_the_array_itself(monkeypatch):
    """No container: the body receives the array, and so does the next call.

    An earlier design returned a `ValidatedPayload` so a nested call could recognise the
    value as already canonical. It required every body in between to know about the box,
    and it is gone. Canonicalizing again is the honest cost of not having it; a caller
    that wants to avoid it passes `skip_digestion=True`, which is what that is for.
    """

    puw.configure.reset()
    puw.configure.load_library(["pint"])
    try:
        puw.register_fast_track("nanometers", puw.unit("nm"))
    except Exception:
        pass

    call_count = {"n": 0}
    original = puw.fast_track.to_nanometers

    def counted(value, parser=None):
        call_count["n"] += 1
        return original(value, parser=parser)

    monkeypatch.setattr(puw.fast_track, "to_nanometers", counted)

    @arg_digest.map(coord={"kind": "q", "rules": [puw_support.nm_float64(ndim=1)]})
    def kernel(coord):
        return coord

    q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    output = kernel(q)

    assert isinstance(output, np.ndarray)
    assert output.dtype == np.float64
    assert output.tolist() == pytest.approx([0.1, 0.2])
    assert call_count["n"] == 1


@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_the_registered_science_pipeline_yields_a_naked_array():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    # Manually register fast-track for tests because they use a fresh puw import
    try:
        puw.register_fast_track("nanometers", puw.unit("nm"))
    except:
        pass

    @arg_digest.map(coord={"kind": "sci", "rules": ["nm_float64"]})
    def kernel(coord):
        return coord

    q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    output = kernel(q)

    assert output.dtype == "float64"
    assert output.shape == (2,)
    assert output.tolist() == pytest.approx([0.1, 0.2])


@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_canonical_pipeline_ndim_mismatch_raises():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    # Manually register fast-track for tests because they use a fresh puw import
    try:
        puw.register_fast_track("nanometers", puw.unit("nm"))
    except:
        pass

    @arg_digest.map(coord={"kind": "q", "rules": [puw_support.nm_float64(ndim=2)]})
    def kernel(coord):
        return coord

    q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    with pytest.raises(DigestValueError, match="expected ndim=2"):
        kernel(q)
