# Proposal: Selective JS ↔ Python Customs Aduana (`argdigest.bridge`)

## Abstract

We propose introducing `argdigest.bridge`, a specialized sub-module for validating and tracking structured signals passing through WebSocket boundaries (e.g., Jupyter Widgets). This includes the `@arg_digest.bridge_receiver` decorator for incoming events and the `BridgeEmitter` utility for outgoing JSON payloads.

This addresses the risk of silent state corruption when the frontend (JS/TS) sends mutated, incorrect, or mismatched events to the Python backend.

---

## The Problem

In interactive web widgets like `molsysviewer`, signals travel back and forth over a WebSocket bridge. 
While public Python methods are validated via `@arg_digest`, incoming events from JavaScript/TypeScript (e.g., in Jupyter callbacks like `on_msg`) are completely unvalidated.
* If a TypeScript release updates its payload (e.g., sending atom indices as strings instead of 0-based integers, or renaming a key).
* Python accepts the payload blindly, silently corrupting internal registries (`self._regions`, `self._layers`).
* This triggers extremely hard-to-debug crashes or logical errors far downstream in the scientific core.

However, running heavy JSON Schema or Pydantic validation on *all* WebSocket messages would destroy performance, particularly for high-frequency interaction signals like hover coordinates or camera adjustments.

---

## Proposed Solution

Introduce a performance-aware, selective validation gateway:

### 1. The `@arg_digest.bridge_receiver` Decorator
For Jupyter callbacks handling incoming JS events (e.g., `_handle_custom_msg`):
```python
@arg_digest.bridge_receiver(schema="viewer_messages.json")
def _on_frontend_event(self, content: dict, buffers):
    # Process the message
    pass
```
* **Selective Validation**: It only validates structural, state-changing messages (e.g., `region_deleted`, `layer_ack`). It **skips** high-frequency, telemetry-heavy events (like `interaction_hover` or camera updates) to prevent interface lagging.
* **Diagnostics**: If an event violates the schema, it raises a catalog-driven exception, immediately pointing out the mismatch.

### 2. The `BridgeEmitter` class (Outgoing payloads)
A clean, typed message emitter that ensures Python-constructed JSON perfectly matches the TypeScript interface contracts defined in `viewer-messages.ts`, automatically coercing PyUnitWizard structures (e.g. converting space dimensions to the mandatory Angstroms required by TS).

### 3. Production Bypass (Zero-Cost Runtime)
The bridge validation is strictly bound to development:
* **Active**: Only when `smonitor.PROFILE == "development"`.
* **Bypassed**: When `smonitor.PROFILE == "user"` (production mode), the decorator acts as a direct passthrough with **absolute zero latency**, ensuring interactive visualization frames remain butter-smooth.

---

## Benefits

* **State Safety**: Prevents corrupted JS events from polluting Python data structures.
* **Contract Sync**: Keeps Python and TypeScript message schemas in perfect harmony.
* **Optimal Latency**: Highly-targeted and active only during development, maintaining pristine high-frequency frame rates in production.
