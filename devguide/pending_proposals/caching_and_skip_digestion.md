# Proposal: Automated Library Bypass and SMonitor Profile Coupling

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
