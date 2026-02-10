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
    },
    "warnings": {
        "DigestNotDigestedWarning": {
            "code": "ARG-WARN-MISS-001",
            "source": "argdigest.warning.missing",
            "category": "argument",
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
        "user_hint": "{hint} Docs: {doc_url}",
        "dev_message": "Digester missing for '{argname}' in '{caller}'.",
        "dev_hint": "Implement digester. {hint}",
    }
}

SIGNALS = {
    "argdigest.error.type": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.error.value": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.error.invariant": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.error.missing": {"extra_required": ["argname", "message", "caller"]},
    "argdigest.warning.missing": {"extra_required": ["argname", "caller"]},
}