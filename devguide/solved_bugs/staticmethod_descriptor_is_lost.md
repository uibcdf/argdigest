---
summary: Preserve staticmethod semantics in both decorator orders and access paths.
issue: uibcdf/argdigest#39
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [decoration, inheritance, binding]
guard: tests/test_contract_owner.py::test_inherited_descriptor_contract_identity
normative:
blocked_by: []
supersedes: []
---

# Staticmethod descriptor is lost

## Completion — 2026-10-22

The complete source suite passes 456 tests without omissions. The guard
includes twelve descriptor/ownership combinations and checks both class and
instance access. The two reverse-order explicit-owner instance calls failed
before the fix, independently of their successful class calls. This directly
protects descriptor binding while retaining existing classmethod handling.

## What

With `@arg_digest` outside `@staticmethod`, instance access binds a receiver to
the returned ordinary function. Class access can succeed, hiding the defect.

## How

Two initial new checks at `ca172d68a78190836031d0602580bd6a2203a9d2`
reproduce `TypeError: too many positional arguments` through an inherited
instance, under definition and exact ownership. Earlier tests exercised only
the other staticmethod order and class access.

The decorator now unwraps and restores staticmethod at the same boundary where
it already handles classmethod. Existing classmethod handling is retained.
The guard checks both orders through both class and instance access under all
three ownership modes. Static functions have no receiver: their diagnostic
qualified name remains definition-based, rather than inventing a runtime class.

## Why

Contract ownership must not alter Python descriptor binding. This is a
descriptor-preservation fix, with no need for another ownership mode or API.

## Acceptance criteria

- Class and instance access both work in each staticmethod decorator order.
- Both classmethod orders retain behavior and runtime display.
- Default, definition and exact ownership remain covered.
