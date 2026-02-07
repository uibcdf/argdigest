# ArgDigest Roadmap

This document outlines the development phases and future goals for **ArgDigest**.

## 🧭 Development Roadmap

| Phase | Objectives | Status | Key Deliverables |
|:------|:-----------|:-------|:-----------------|
| **v0.1 (Prototype)** | Functional `@arg_digest` decorator + minimal registry | **Done** | Core pipeline, argument-centric mode, `arg_digest.map` |
| **v0.2.0** | Context-aware error system + logging | **Done** | Rich exceptions, logging, native Pydantic/Beartype |
| **v0.3.0** | Standard Pipelines & Science Integration | **Done** | Built-in pipelines, PyUnitWizard integration, legacy compat |
| **v0.4.0** | Declarative Config & Advanced Features | **Done** | YAML/JSON rules, Numpy/Pandas support, Profiling |
| **v0.5.0** | Performance & Telemetry | **Done** | Digestion Plan Caching, `@signal` integration, LRU caching |
| **v0.6.0** | Pilot Integration (MolSysMT) | **In Progress** | Replace legacy engine in MolSysMT key modules |
| **v1.0.0** | Stable API + >90% coverage + Release | **Pending** | 1.0.0 release, full CI/CD, PyPI/Conda distribution |

---

## 🏗️ Future Goals & Ideas

### Core Infrastructure
- **CLI Audit Tool**: Standalone command to scan scripts and libraries (`argdigest audit script.py`).
- **Declarative Validation**: Support for `JSONSchema` or `YAML` based pipeline definitions.
- **Undo Hooks**: Capability to revert coercions for reversible transformations.

### Science & Data Integration
- **Advanced Numpy/Pandas Pipelines**: Deeper semantic validation for multi-dimensional data structures.
- **Distributed Telemetry**: Integration with external observability tools for large-scale analytics.

### Documentation & UX
- **Sphinx Extension**: Automatically document argument validation logic in API references.
- **AI-Agent Instructions**: Export digestion plans as structured context for LLM agents.

---
> **ArgDigest** — building the foundation for reliable scientific Python interfaces.