from argdigest.core.caller import caller_is_one_of, caller_matches, caller_startswith, normalize_caller


def sample_function():
    return None


def test_normalize_caller_accepts_strings_and_callables():
    assert normalize_caller(" package.fn ") == "package.fn"
    assert normalize_caller(sample_function).endswith("sample_function")
    assert normalize_caller(None) is None
    assert normalize_caller(None, fallback="unknown") == "unknown"


def test_caller_matches_handles_missing_caller_safely():
    assert caller_matches(None, "foo") is False
    assert caller_matches("pkg.mod.add_contacts", "add_contacts") is True
    assert caller_matches(sample_function, "sample_function") is True


def test_caller_is_one_of_handles_normalization():
    assert caller_is_one_of("pkg.mod.fn", ["pkg.mod.fn", "other"]) is True
    assert caller_is_one_of(None, ["pkg.mod.fn"]) is False



def test_caller_startswith_handles_normalization():
    assert caller_startswith("pkg.form.converter", "pkg.form") is True
    assert caller_startswith(sample_function, "test_") is False
    assert caller_startswith(None, "pkg") is False
