from __future__ import annotations

from pathlib import Path

from .meta import DOC_URL, ISSUES_URL, API_URL

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

META = {
    "doc_url": DOC_URL,
    "issues_url": ISSUES_URL,
    "api_url": API_URL,
}

CATALOG = {
    "exceptions": {
        "DigestTypeError": {
            "code": "ARG-ERR-TYPE-001",
            "source": "argdigest.error.type",
            "category": "argument",
            "level": "ERROR",
        },
        "DigestValueError": {
            "code": "ARG-ERR-VAL-001",
            "source": "argdigest.error.value",
            "category": "argument",
            "level": "ERROR",
        },
        "DigestInvariantError": {
            "code": "ARG-ERR-INV-001",
            "source": "argdigest.error.invariant",
            "category": "argument",
            "level": "ERROR",
        },
        "DigestNotDigestedError": {
            "code": "ARG-ERR-MISS-001",
            "source": "argdigest.error.missing",
            "category": "argument",
            "level": "ERROR",
        },
        "UnknownArgumentError": {
            "code": "ARG-ERR-CONTRACT-001",
            "source": "argdigest.error.contract.unknown_argument",
            "category": "contract",
            "level": "ERROR",
        },
        "MissingArgumentError": {
            "code": "ARG-ERR-CONTRACT-002",
            "source": "argdigest.error.contract.missing_argument",
            "category": "contract",
            "level": "ERROR",
        },
        "ArgumentConsistencyError": {
            "code": "ARG-ERR-CONTRACT-003",
            "source": "argdigest.error.contract.consistency",
            "category": "contract",
            "level": "ERROR",
        },
    },
    "warnings": {
        "DigestNotDigestedWarning": {
            "code": "ARG-WARN-MISS-001",
            "source": "argdigest.warning.missing",
            "category": "argument",
            "level": "WARNING",
        },
        "FunctionContractWarning": {
            "code": "ARG-WARN-CONTRACT-001",
            "source": "argdigest.warning.contract",
            "category": "contract",
            "level": "WARNING",
        },
        "TypeCheckSkippedWarning": {
            "code": "ARG-WARN-TYPECHECK-001",
            "source": "argdigest.warning.typecheck_skipped",
            "category": "dependency",
            "level": "WARNING",
        },
    }
}

CODES = {
    "ARG-ERR-TYPE-001": {
        "title": "Argument Type Error",
        "user_message": "Type mismatch for argument '{argname}'. {message}",
        "user_hint": "Check the expected type in the docs. {hint} Docs: {doc_url}",
        "dev_message": "Type error in '{caller}' for '{argname}': {message}",
        "dev_hint": "Validate type logic. {hint}",
    },
    "ARG-ERR-VAL-001": {
        "title": "Argument Value Error",
        "user_message": "Invalid value for argument '{argname}'. {message}",
        "user_hint": "Check the valid values. {hint} Docs: {doc_url}",
        "dev_message": "Value error in '{caller}' for '{argname}': {message}",
        "dev_hint": "Validate value constraints. {hint}",
    },
    "ARG-ERR-INV-001": {
        "title": "Argument Invariant Error",
        "user_message": "Invariant violation for argument '{argname}'. {message}",
        "user_hint": "Check relationships between arguments. {hint} Docs: {doc_url}",
        "dev_message": "Invariant error in '{caller}': {message}",
        "dev_hint": "Check inter-argument constraints. {hint}",
    },
    "ARG-ERR-MISS-001": {
        "title": "Argument Not Digested Error",
        "user_message": "Digester missing or cyclic dependency for '{argname}'. {message}",
        "user_hint": "Report this internal issue. {hint} Docs: {doc_url}",
        "dev_message": "Missing digester for '{argname}' in '{caller}'.",
        "dev_hint": "Implement digester or check cycles. {hint}",
    },
    "ARG-WARN-MISS-001": {
        "title": "Argument Not Digested Warning",
        "user_message": "Digester missing for '{argname}'. Skipping validation.",
        "user_hint": "Define or register a digester for '{argname}'. Docs: {doc_url}",
        "dev_message": "Digester missing for '{argname}' in '{caller}'.",
        "dev_hint": "Implement or register the missing digester.",
    },
    "ARG-ERR-CONTRACT-001": {
        "title": "Unknown argument",
        "user_message": "{message}",
        "user_hint": "{hint} Docs: {doc_url}",
        "dev_message": "Argument '{argname}' is outside the declared contract of '{caller}'.",
        "dev_hint": "Extend the function contract if the argument is legitimate. {hint}",
    },
    "ARG-ERR-CONTRACT-002": {
        "title": "Missing required argument",
        "user_message": "{message}",
        "user_hint": "{hint} Docs: {doc_url}",
        "dev_message": "Call to '{caller}' satisfies no required argument group.",
        "dev_hint": "Check 'requires_any_of' in the function contract. {hint}",
    },
    "ARG-ERR-CONTRACT-003": {
        "title": "Inconsistent arguments",
        "user_message": "{message}",
        "user_hint": "{hint} Docs: {doc_url}",
        "dev_message": "Call to '{caller}' breaks an inter-argument rule.",
        "dev_hint": "Check 'mutually_exclusive' and 'co_required'. {hint}",
    },
    "ARG-WARN-CONTRACT-001": {
        "title": "Function contract violation",
        "user_message": "{message}",
        "user_hint": "{hint} Docs: {doc_url}",
        "dev_message": "Contract violation in '{caller}': {message}",
        "dev_hint": "The unknown_argument policy is set to 'warn'. {hint}",
    },
    "ARG-WARN-TYPECHECK-001": {
        "title": "Type check skipped",
        "user_message": "Type checks are disabled because optional dependency 'beartype' is not available.",
        "user_hint": "Install 'beartype' to enable runtime type checking.",
        "dev_message": "type_check=True but 'beartype' is not installed in '{caller}'.",
        "dev_hint": "Install beartype or set type_check=False.",
    },
}

SIGNALS = {
    "argdigest.error.type": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.error.value": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.error.invariant": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.error.missing": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.warning.missing": {"extra_required": ["argname", "caller"]},
    "argdigest.warning.typecheck_skipped": {"extra_required": ["caller"]},
}
