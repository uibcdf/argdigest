# Proposal: Automated Library Bypass and SMonitor Profile Coupling

> **Declined 2026-08-12, on measurement.** The +5.25 ms is real; the diagnosis is not.
> ArgDigest's own plumbing is **21.6 µs per call and flat** — 0.4% of the reported
> overhead. The cost is one MolSysMT predicate, `has_attribute`, wearing a
> boundary-grade digester nine times its own weight and being called **434 times per
> `regions.add`** (~29 ms). Filed as `uibcdf/molsysmt` →
> `devguide/pending_bugs/boundary_digestion_on_internal_predicates.md`, with the
> attribution in MolSysViewer's `devguide/performance/argdigest_overhead_attribution_2026_08.md`.
>
> Three reasons, any one sufficient:
>
> 1. **Digestion transforms values; it does not only check them.** `to_numpy`,
>    `convert(to_unit=...)`, form assessment. Bypassing does not skip a check — it
>    changes what the function receives, so production would run a different program
>    from the one tested. Unlike `assert` under `-O`, which guards internal invariants
>    and alters no value.
> 2. **It removes the check from the population it was built for.** The 0.10.0 note is
>    explicit: the typo defect only ever reached users. Developers write correct calls;
>    they wrote the API. Validating in `dev` and not in `user` validates the wrong people.
> 3. **It would have hidden the real defect.** The number would have dropped and the 434
>    redundant calls would have stayed. The overhead was a symptom pointing at a bug, and
>    the proposal would have removed the symptom.
>
> Also, on the details: the profile names here (`production`/`development`) are not
> ArgDigest's (`user`/`dev`/`qa`/`agent`/`debug`); the signature shown is not the real
> one; and reading the profile at decoration time would freeze it against any later
> `smonitor.configure(profile=...)`.
>
> **What replaces it.** The motivating case — a canonical value reused across many calls
> — was going to be served by value certification, then under design. It was built,
> measured and **declined the next day**
> ([`value_certification/`](value_certification/README.md)): it asked every digester
> author to learn three concepts for a problem no consumer had. What actually served the
> case was the cheap canonicity predicate PyUnitWizard shipped the same day, which took
> `puw.check(q, unit='nm')` from 887 µs to 10.26 and let a digester short-circuit in two
> lines with no mechanism at all. For call sites you control, `skip_digestion` remains
> the cheapest tool at 1.8 µs. The `bypass_validation` context manager is not adopted:
> its scope is non-local, silently covering callees the block's author does not know are
> decorated.

## Abstract

We propose introducing an internal validation bypass mechanism (`arg_digest.bypass_validation`) and automatic SMonitor profile-driven short-circuiting to `argdigest`. Instead of placing the burden of performance optimization on the end-user (e.g. through explicit user-facing "turbo" flags), the validation framework will silently and automatically bypass validations on hot paths during production execution or controlled internal loops, achieving zero-cost execution speeds with absolute user-facing simplicity.

---

## The Problem

ArgDigest provides excellent validation safety, but performance benchmarks show it introduces a noticeable overhead on high-frequency API operations:
* **Baseline (None)**: ~21.06 ms mean latency.
* **ArgDigest-only**: ~26.30 ms mean latency (+5.25 ms, **24.9% slowdown**).

During dynamic trajectory playback or high-frequency rendering, repeating complete validation steps for every frame is redundant. However:
1. **User-facing optimization switches** (like a hypothetical `msv.fast_path()`) are bad API design. They shift architectural burdens to scientific users, who expect code to be both correct and fast by default.
2. **Hard-coded bypasses** reduce safety globally, leaving no way for developers to catch issues during integration testing or troubleshooting.

We need a silent, framework-level solution that operates automatically without user awareness.

---

## Proposed Solution

We propose a two-layered, fully automated optimization architecture:

### 1. SMonitor Profile-Driven Short-Circuiting
ArgDigest can read the active SMonitor profile during initialization. When SMonitor is in the default `"production"` profile (intended for normal scientific usage), ArgDigest will automatically bypass dynamic signature inspection and parameter shape/unit checks on decorators marked as `high_frequency=True`:

```python
# argdigest/decorators.py
import smonitor

def arg_digest(*rules, high_frequency=False):
    def decorator(func):
        # Cache check status at import/decoration time
        is_production = getattr(smonitor, "PROFILE", "production") == "production"
        should_bypass = high_frequency and is_production
        
        def wrapper(*args, **kwargs):
            if should_bypass or getattr(_local_state, "bypass_active", False):
                # Total zero-overhead passthrough on the user's hot path
                return func(*args, **kwargs)
            
            # Run standard validation for development profile
            return run_validation(func, rules, args, kwargs)
        return wrapper
    return decorator
```

This guarantees that in the default user environment, high-frequency actions like coordinate updates are executed with **absolute zero validation overhead**, while during development (`smonitor.PROFILE == "development"`), the robust safety net is fully active to catch bugs.

### 2. Internal Developer-Facing `bypass_validation` Context Manager
For complex internal library loops (such as trajectory playback animations implemented within `molsysviewer` or other client packages), developers can explicitly wrap hot-path execution blocks. This is purely an internal framework tool, completely hidden from the public-facing user API:

```python
# argdigest/context.py
import threading

_local_state = threading.local()

class bypass_validation:
    """Internal developer context manager to temporarily suspend validation checks."""
    def __enter__(self):
        self.previous = getattr(_local_state, "bypass_active", False)
        _local_state.bypass_active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _local_state.bypass_active = self.previous
```

#### Internal usage example (Hidden inside MolSysViewer):
```python
# molsysviewer/viewer/load.py (Internal playback loop)
from argdigest import bypass_validation

def _play_trajectory_loop(self):
    # Hide the validation bypass from the user
    with bypass_validation():
        for frame_coords in self._trajectory_frames:
            self._update_coordinates_direct(frame_coords)
```

---

## Benefits

* **Zero User Burden**: The end-user writes standard pythonic code, completely unaware of validation configurations, while enjoying baseline-level rendering speeds.
* **Invisible Telemetry Alignment**: ArgDigest automatically scales its validation behavior to match the active SMonitor profile.
* **Safe Development Auditing**: Full validation remains active for developers running in the `development` profile, catching contract mismatches before releases.
