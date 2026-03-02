# User

Welcome. This guide is a practical adoption path for developers integrating
ArgDigest into their own libraries.

If you follow the pages in order, you will move from a first working setup to
production-ready integration patterns.

The main audience is library integrators, but this section also includes one
page for end users who consume libraries that already integrate ArgDigest.

Before implementation, keep the contract guide at hand:
- [ARG_DIGEST_AGENTS.md](https://github.com/uibcdf/argdigest/blob/main/ARG_DIGEST_AGENTS.md)

## Fast Track (20 minutes)

If you want the minimum path first, read in this order:
1. [What ArgDigest Solves](what-argdigest-solves.md)
2. [Quick Start](quickstart.md)
3. [Configuration](configuration.md)
4. [Integrating Your Library](integrating-your-library.md)
5. [Production Checklist](production-checklist.md)

## Learning Path

1. [What ArgDigest Solves](what-argdigest-solves.md): scope, value, and non-goals.
2. [Quick Start](quickstart.md): first working integration in minutes.
3. [Integration Cheat Sheet](integration-cheat-sheet.md): copy-ready minimal setup.
4. [Mini Library Walkthrough](mini-library-walkthrough.md): complete narrative from zero to production shape.
5. [Configuration](configuration.md): how `_argdigest.py` defines defaults and policy.
6. [Configuration Precedence](config-precedence.md): exact resolution order and override rules.
7. [Digestion Styles](digestion-styles.md): package, registry, decorator, and mixed approaches.
8. [Auto Mode and Conflict Resolution](auto-and-conflicts.md): how `auto` chooses digesters and how to avoid ambiguity.
9. [Normalization](normalization.md): argument name standardization before digestion.
10. [skip_digestion Behavior](skip-digestion.md): bypass semantics and safe usage.
11. [Pipeline Design Patterns](pipeline-design.md): robust rule design and context usage.
12. [Strictness and Errors](strictness-and-errors.md): warning/error behavior and troubleshooting signals.
13. [Migration: warn to error](migration-warn-to-error.md): staged hardening criteria.
14. [Integrating Your Library](integrating-your-library.md): migration blueprint for real codebases.
15. [Examples](examples.md): where to find copy-ready integration scenarios.
16. [Troubleshooting](troubleshooting.md): quick diagnosis for common failures.
17. [Production Checklist](production-checklist.md): final pre-release verification.
18. [For End Users of Integrating Libraries](end-users.md): how to interpret validation messages in real usage.
19. [FAQ](faq.md): short answers to recurring adoption questions.

```{toctree}
:maxdepth: 1
:hidden:

what-argdigest-solves.md
quickstart.md
integration-cheat-sheet.md
mini-library-walkthrough.md
configuration.md
config-precedence.md
digestion-styles.md
auto-and-conflicts.md
normalization.md
skip-digestion.md
pipeline-design.md
strictness-and-errors.md
migration-warn-to-error.md
integrating-your-library.md
examples.md
troubleshooting.md
production-checklist.md
end-users.md
faq.md
```
