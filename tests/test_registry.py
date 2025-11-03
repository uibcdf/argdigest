from argdigest.core.registry import Registry, register_pipeline

def test_registry():
    @register_pipeline(kind="foo", name="bar")
    def foo_bar(v, ctx):
        return v

    assert "foo" in Registry._pipelines
    assert "bar" in Registry._pipelines["foo"]

