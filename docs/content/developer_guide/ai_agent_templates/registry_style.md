# Template: Registry-style digestion

Use this template when the library prefers a central registry rather than one file per argument.

## Goal
- Define a module exposing `ARGUMENT_DIGESTERS`.
- ArgDigest discovers digesters via `digestion_style="registry"`.

## Required structure
```
my_lib/
  _argdigest.py
  _private/
    digestion/
      registry.py
```

## Library config (`my_lib/_argdigest.py`)
```python
DIGESTION_SOURCE = "my_lib._private.digestion.registry"
DIGESTION_STYLE = "registry"
STRICTNESS = "warn"
SKIP_PARAM = "skip_digestion"
```

## Registry module (`registry.py`)
```python
def digest_a(a, caller=None):
    return int(a)


def digest_b(b, a=None, caller=None):
    return int(b) + int(a)


ARGUMENT_DIGESTERS = {
    "a": digest_a,
    "b": digest_b,
}
```

## Usage in public API
```python
from argdigest import digest

@digest(config="my_lib._argdigest")
def analyze(a, b, skip_digestion=False):
    ...
```
