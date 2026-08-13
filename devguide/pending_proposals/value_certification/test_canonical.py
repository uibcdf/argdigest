"""Value certification: the claim travels with the value and dies with it.

Stage 1 of replacing the passport wrapper. These tests hold the module on its own,
before it is wired into the decorator.
"""

import gc
import threading

import numpy as np
import pytest

from argdigest.core.canonical import (
    GUARD_FORM,
    GUARD_FROZEN,
    GUARD_IDENTITY,
    certify,
    claim_count,
    claim_for,
    clear_claims,
    revoke,
)


@pytest.fixture(autouse=True)
def _clear():
    clear_claims()
    yield
    clear_claims()


def digester_a(value):
    return value


def digester_b(value):
    return value


# --- the value is returned as itself ------------------------------------------------

def test_certify_returns_the_very_same_object():
    array = np.zeros((4, 3))
    assert certify(array, by=digester_a, unit="nm") is array


def test_the_value_keeps_its_type():
    """The point of not wrapping: nothing downstream has to know this happened."""

    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")
    assert isinstance(array, np.ndarray)


def test_the_claim_travels_through_a_function_body():
    """What the wrapper could not do: survive being passed through a body."""

    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")

    def passes_it_on(value):
        return value

    assert claim_for(passes_it_on(passes_it_on(array)), by=digester_a) is not None


def test_a_copy_does_not_inherit_the_claim():
    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")

    assert claim_for(array.copy()) is None


# --- a claim names the verification it represents -----------------------------------

def test_a_claim_is_honoured_only_for_the_digester_that_issued_it():
    """The defect this replaces: any claim silenced any digester of that argument name."""

    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")

    assert claim_for(array, by=digester_a) is not None
    assert claim_for(array, by=digester_b) is None


def test_asking_without_naming_a_digester_returns_whatever_is_held():
    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")
    claim = claim_for(array)

    assert claim is not None
    assert claim.by is digester_a
    assert claim.attributes == {"unit": "nm"}


def test_by_is_required():
    with pytest.raises(TypeError):
        certify(np.zeros(3), unit="nm")


# --- it does not seize what it did not produce --------------------------------------

def test_a_produced_value_is_certified_even_when_source_is_given():
    raw = [[1.0, 2.0, 3.0]]
    produced = certify(np.asarray(raw, dtype=np.float64), by=digester_a,
                       source=raw, unit="nm")

    assert claim_for(produced, by=digester_a) is not None


def test_a_non_array_needs_nothing_declared():
    """Nothing is frozen, so there is nothing to seize and nothing to declare."""

    class System:
        pass

    assert claim_for(certify(System(), by=digester_a), by=digester_a) is not None


# --- the default guard: form ---------------------------------------------------------

def test_the_default_guard_leaves_the_value_untouched():
    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")

    assert array.flags.writeable, "the default must not make the caller's array read-only"
    assert claim_for(array).guard == GUARD_FORM


def test_a_form_claim_survives_an_in_place_value_change():
    """MolSysMT rotates coordinates in place, and rotating nm float64 (n,3) leaves it
    nm float64 (n,3). A form guarantee is still true, so the claim must hold."""

    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm", dtype_name="float64")
    array[0, 0] = 1.5                       # exactly what `structure/rotate.py` does

    assert claim_for(array, by=digester_a) is not None


def test_a_form_claim_is_revoked_by_a_reshape():
    array = certify(np.zeros((6, 3)), by=digester_a, unit="nm")
    array.shape = (3, 6)

    assert claim_for(array) is None


def test_a_form_claim_is_revoked_by_a_dtype_change():
    array = certify(np.zeros((6, 3)), by=digester_a, unit="nm")
    claim_for(array)                        # held
    array.dtype = np.float32

    assert claim_for(array) is None


# --- the opt-in guard: frozen --------------------------------------------------------

def test_the_frozen_guard_makes_the_array_read_only():
    array = certify(np.zeros((4, 3)), by=digester_a, guard=GUARD_FROZEN, source=None,
                    finite=True)

    assert not array.flags.writeable
    with pytest.raises(ValueError):
        array[0, 0] = 1.0


def test_unfreezing_revokes_a_frozen_claim():
    array = certify(np.zeros((4, 3)), by=digester_a, guard=GUARD_FROZEN, source=None,
                    finite=True)
    array.flags.writeable = True

    assert claim_for(array) is None


def test_frozen_revocation_is_destructive_so_refreezing_does_not_resurrect_it():
    """Observing it writeable drops the claim; putting the flag back must not help."""

    array = certify(np.zeros((4, 3)), by=digester_a, guard=GUARD_FROZEN, source=None,
                    finite=True)
    array.flags.writeable = True
    assert claim_for(array) is None          # observed here
    array[0, 0] = np.nan
    array.flags.writeable = False

    assert claim_for(array) is None


def test_freezing_a_value_the_digester_did_not_produce_is_refused():
    """The failure mode of getting this wrong is a ValueError in the *caller's* code."""

    with pytest.raises(TypeError, match="needs 'source'"):
        certify(np.zeros((4, 3)), by=digester_a, guard=GUARD_FROZEN, finite=True)


def test_freezing_declines_when_the_digester_returned_its_own_input():
    """`np.asarray` returns the same object when no conversion is needed."""

    caller_owns_this = np.zeros((4, 3))
    result = certify(np.asarray(caller_owns_this), by=digester_a, guard=GUARD_FROZEN,
                     source=caller_owns_this, finite=True)

    assert result is caller_owns_this
    assert caller_owns_this.flags.writeable, "the caller's array must not be frozen"
    assert claim_for(caller_owns_this) is None


def test_a_view_of_a_certified_array_carries_no_claim_of_its_own():
    array = certify(np.zeros((6, 3)), by=digester_a, unit="nm")

    assert claim_for(array[2:4]) is None


# --- values that cannot be frozen ---------------------------------------------------

def test_a_non_array_object_is_certified_on_identity_alone():
    class System:
        pass

    system = certify(System(), by=digester_a, form="MolSys")
    claim = claim_for(system, by=digester_a)

    assert claim is not None
    assert claim.guard == GUARD_IDENTITY


def test_an_array_records_the_form_guard_by_default():
    array = certify(np.zeros(3), by=digester_a, unit="nm")

    assert claim_for(array).guard == GUARD_FORM


def test_a_value_that_cannot_be_weakly_referenced_is_simply_not_certified():
    """int, str and tuple refuse weak references -- and are cheap to digest anyway."""

    assert certify((1, 2, 3), by=digester_a, unit="nm") == (1, 2, 3)
    assert claim_for((1, 2, 3)) is None


# --- the claim dies with the value --------------------------------------------------

def test_the_claim_is_dropped_when_the_value_is_collected():
    array = certify(np.zeros((4, 3)), by=digester_a, unit="nm")
    assert claim_count() == 1

    del array
    gc.collect()

    assert claim_count() == 0


def test_a_recycled_address_does_not_inherit_a_dead_claim():
    """`id()` alone would be unsound; the weak reference is what closes it."""

    for _ in range(50):
        certify(np.zeros((4, 3)), by=digester_a, unit="nm")
        gc.collect()

    assert claim_count() <= 1


def test_revoke_removes_a_claim_and_reports_whether_there_was_one():
    array = certify(np.zeros(3), by=digester_a, unit="nm")

    assert revoke(array) is True
    assert revoke(array) is False
    assert claim_for(array) is None


# --- introspection -------------------------------------------------------------------

def test_a_claim_renders_as_plain_data():
    array = certify(np.zeros((4, 3)), by=digester_a,
                    issued_by="mylib.basic.get", unit="nm", dtype_name="float64")
    described = claim_for(array).describe()

    assert described["by"] == "digester_a"
    assert described["guard"] == GUARD_FORM
    assert described["shape"] == (4, 3)
    assert described["issued_by"] == "mylib.basic.get"
    assert described["attributes"]["unit"] == "nm"


# --- concurrency ---------------------------------------------------------------------

def test_certifying_from_several_threads_keeps_the_registry_consistent():
    arrays = [np.zeros(3) for _ in range(200)]
    errors: list[BaseException] = []

    def worker(chunk):
        try:
            for array in chunk:
                certify(array, by=digester_a, unit="nm")
                assert claim_for(array, by=digester_a) is not None
        except BaseException as error:      # noqa: BLE001 - reported, not swallowed
            errors.append(error)

    threads = [threading.Thread(target=worker, args=(arrays[i::4],)) for i in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert not errors
    assert claim_count() == len(arrays)
