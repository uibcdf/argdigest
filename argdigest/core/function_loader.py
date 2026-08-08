"""Discovery of axis-1 declarations: function contracts and named domains.

This mirrors `argument_loader` on purpose. A consumer already knows how to declare
per-argument digesters by dropping one module per argument into a package; declaring a
function contract or a domain should not require learning a second idiom.

A module in the function source declares `contract` or `CONTRACTS`. A module in the
domain source declares `domain` or `DOMAINS`. A module in the normalization source
declares `table` or `TABLES`. Nothing else is imposed on the consumer: scanning,
ordering, and validation happen here.
"""

from __future__ import annotations

import pkgutil
from functools import lru_cache
from importlib import import_module
from types import ModuleType
from typing import Iterable

from .function_contract import ContractRegistry, Domain, FunctionContract
from .normalization import AliasTable, NormalizationRegistry


def _coerce_sources(source: str | Iterable[str] | None) -> list[str]:
    if source is None:
        return []
    if isinstance(source, str):
        return [source]
    return list(source)


def _iter_package_modules(package_path: str) -> list[ModuleType]:
    package = import_module(package_path)
    if not hasattr(package, "__path__"):
        return [package]
    modules = []
    for module_info in sorted(pkgutil.iter_modules(package.__path__), key=lambda item: item.name):
        modules.append(import_module(f"{package_path}.{module_info.name}"))
    return modules


def _collect_contracts(module: ModuleType) -> list[FunctionContract]:
    collected: list[FunctionContract] = []
    single = getattr(module, "contract", None)
    if isinstance(single, FunctionContract):
        collected.append(single)
    many = getattr(module, "CONTRACTS", None)
    if many is not None:
        for item in many:
            if not isinstance(item, FunctionContract):
                raise TypeError(
                    f"{module.__name__}.CONTRACTS must contain FunctionContract instances; "
                    f"got {type(item).__name__}."
                )
            collected.append(item)
    return collected


def _collect_domains(module: ModuleType) -> list[Domain]:
    collected: list[Domain] = []
    single = getattr(module, "domain", None)
    if isinstance(single, Domain):
        collected.append(single)
    many = getattr(module, "DOMAINS", None)
    if many is not None:
        for item in many:
            if not isinstance(item, Domain):
                raise TypeError(
                    f"{module.__name__}.DOMAINS must contain Domain instances; "
                    f"got {type(item).__name__}."
                )
            collected.append(item)
    return collected


@lru_cache(maxsize=None)
def load_function_contracts(function_source: str | tuple[str, ...] | None) -> ContractRegistry:
    """Build the contract registry declared by a consumer."""

    registry = ContractRegistry()
    for source in _coerce_sources(function_source):
        for module in _iter_package_modules(source):
            for contract in _collect_contracts(module):
                registry.add(contract)
    return registry


@lru_cache(maxsize=None)
def load_domains(domain_source: str | tuple[str, ...] | None) -> dict[str, Domain]:
    """Build the domain table declared by a consumer."""

    domains: dict[str, Domain] = {}
    for source in _coerce_sources(domain_source):
        for module in _iter_package_modules(source):
            for domain in _collect_domains(module):
                domains[domain.name] = domain
    return domains


def _collect_alias_tables(module: ModuleType) -> list[AliasTable]:
    collected: list[AliasTable] = []
    single = getattr(module, "table", None)
    if isinstance(single, AliasTable):
        collected.append(single)
    many = getattr(module, "TABLES", None)
    if many is not None:
        for item in many:
            if not isinstance(item, AliasTable):
                raise TypeError(
                    f"{module.__name__}.TABLES must contain AliasTable instances; "
                    f"got {type(item).__name__}."
                )
            collected.append(item)
    return collected


@lru_cache(maxsize=None)
def load_normalization(normalization_source: str | tuple[str, ...] | None
                       ) -> NormalizationRegistry:
    """Build the alias registry declared by a consumer."""

    registry = NormalizationRegistry()
    for source in _coerce_sources(normalization_source):
        for module in _iter_package_modules(source):
            for table in _collect_alias_tables(module):
                registry.add(table)
    return registry
