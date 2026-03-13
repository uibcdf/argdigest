import pytest
try:
    import pyunitwizard as puw
    from argdigest.contrib import pyunitwizard_support as puw_support
    from argdigest.contrib.pyunitwizard_support import ValidatedPayload
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
def test_nm_float64_payload_bypasses_redundant_recanonicalization(monkeypatch):
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    # Manually register fast-track for tests because they use a fresh puw import
    try:
        puw.register_fast_track("nanometers", puw.unit("nm"))
    except:
        pass

    call_count = {"n": 0}
    original = puw.fast_track.to_nanometers

    def counted(value, parser=None):
        call_count["n"] += 1
        return original(value, parser=parser)

    monkeypatch.setattr(puw.fast_track, "to_nanometers", counted)

    @arg_digest.map(coord={"kind": "q", "rules": [puw_support.nm_float64_payload(ndim=1)]})
    def inner(coord):
        return coord

    @arg_digest.map(coord={"kind": "q", "rules": [puw_support.nm_float64_payload(ndim=1)]})
    def outer(coord):
        return inner(coord)

    q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    output = outer(q)

    assert isinstance(output, ValidatedPayload)
    assert output.unit == "nm"
    assert output.dtype == "float64"
    assert call_count["n"] == 1


@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_registered_science_pipelines_can_return_naked_array():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    # Manually register fast-track for tests because they use a fresh puw import
    try:
        puw.register_fast_track("nanometers", puw.unit("nm"))
    except:
        pass

    @arg_digest.map(
        coord={
            "kind": "sci",
            "rules": ["nm_float64_payload", "unwrap_validated_payload"],
        }
    )
    def kernel(coord):
        return coord

    q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    output = kernel(q)

    assert output.dtype == "float64"
    assert output.shape == (2,)
    assert output.tolist() == pytest.approx([0.1, 0.2])


@pytest.mark.skipif(not HAS_PUW, reason="pyunitwizard not installed")
def test_payload_pipeline_ndim_mismatch_raises():
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    # Manually register fast-track for tests because they use a fresh puw import
    try:
        puw.register_fast_track("nanometers", puw.unit("nm"))
    except:
        pass

    @arg_digest.map(coord={"kind": "q", "rules": [puw_support.nm_float64_payload(ndim=2)]})
    def kernel(coord):
        return coord

    q = puw.quantity([1.0, 2.0], "angstrom", form="pint")
    with pytest.raises(DigestValueError, match="expected ndim=2"):
        kernel(q)
