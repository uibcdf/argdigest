import pytest
from argdigest import arg_digest, DigestValueError, DigestTypeError

def test_std_coercers_all():
    @arg_arg_digest.map(
        b1={"kind": "std", "rules": ["to_bool"]},
        b2={"kind": "std", "rules": ["to_bool"]},
        l1={"kind": "std", "rules": ["to_list"]},
        l2={"kind": "std", "rules": ["to_list"]},
        t1={"kind": "std", "rules": ["to_tuple"]},
        s1={"kind": "std", "rules": ["strip"]},
        low={"kind": "std", "rules": ["lower"]},
        up={"kind": "std", "rules": ["upper"]}
    )
    def f(b1, b2, l1, l2, t1, s1, low, up):
        return b1, b2, l1, l2, t1, s1, low, up

    res = f("yes", "no", "scalar", [1, 2], "tuple_me", "  spaces  ", "HELLO", "world")
    
    assert res[0] is True
    assert res[1] is False
    assert res[2] == ["scalar"]
    assert res[3] == [1, 2]
    assert res[4] == ("tuple_me",)
    assert res[5] == "spaces"
    assert res[6] == "hello"
    assert res[7] == "WORLD"

def test_to_bool_edge_cases():
    @arg_arg_digest.map(v={"kind": "std", "rules": ["to_bool"]})
    def f(v): return v
    
    assert f("on") is True
    assert f("off") is False
    assert f("1") is True
    assert f(0) is False

def test_std_validators_extended(tmp_path):
    # Create a dummy file and dir
    d = tmp_path / "subdir"
    d.mkdir()
    f_path = d / "test.txt"
    f_path.write_text("content")

    @arg_arg_digest.map(
        pos={"kind": "std", "rules": ["is_positive"]},
        non_neg={"kind": "std", "rules": ["is_non_negative"]},
        file_p={"kind": "std", "rules": ["is_file"]},
        dir_p={"kind": "std", "rules": ["is_dir"]},
        i={"kind": "std", "rules": ["is_int"]},
        s={"kind": "std", "rules": ["is_str"]}
    )
    def validate(pos, non_neg, file_p, dir_p, i, s):
        return True

    assert validate(1, 0, str(f_path), str(d), 42, "hi")

    with pytest.raises(DigestValueError, match="positive"):
        validate(0, 0, str(f_path), str(d), 42, "hi")

    with pytest.raises(DigestValueError, match="non-negative"):
        validate(1, -1, str(f_path), str(d), 42, "hi")

    with pytest.raises(DigestValueError, match="File not found"):
        validate(1, 0, "non_existent.txt", str(d), 42, "hi")

    with pytest.raises(DigestValueError, match="Directory not found"):
        validate(1, 0, str(f_path), "non_existent_dir", 42, "hi")

    with pytest.raises(DigestTypeError, match="Expected int"):
        validate(1, 0, str(f_path), str(d), "not_int", "hi")

    def test_to_list_iterables():

        @arg_arg_digest.map(v={"kind": "std", "rules": ["to_list"]})

        def f(v): return v

        

        assert f((1, 2)) == [1, 2]

        import numpy as np

        res = f(np.array([1, 2]))

        assert isinstance(res, list)

        assert res == [1, 2]

    

    def test_string_coercers_non_string():

        @arg_arg_digest.map(v={"kind": "std", "rules": ["strip", "lower", "upper"]})

        def f(v): return v

        # Should ignore non-string inputs

        assert f(123) == 123

    