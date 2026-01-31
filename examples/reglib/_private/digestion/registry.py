from __future__ import annotations


def digest_a(a, caller=None):
    return int(a)


def digest_b(b, a=None, caller=None):
    return int(b) + int(a)


ARGUMENT_DIGESTERS = {
    "a": digest_a,
    "b": digest_b,
}
