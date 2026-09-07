from __future__ import annotations

from pathlib import Path

from .meta import API_URL, DOC_URL, ISSUES_URL

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
        "OptionalDependencyError": {
            "code": "ARG-ERR-OPTDEP-001",
            "source": "argdigest.error.optional_dependency",
            "category": "dependency",
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
        "StandardizerContractError": {
            "code": "ARG-ERR-STD-001",
            "source": "argdigest.error.standardizer",
            "category": "normalization",
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
    },
}

#: The wording lives here, and only here. A raise site passes typed fields --
#: `detail` for the specific fact it knows, `guess` for a did-you-mean -- and
#: never a rendered sentence: a sentence handed over as `message` bypasses these
#: templates entirely, which is what used to happen and why four of them had been
#: written and never rendered for a single user.
#:
#: `argname`, `caller`, `doc_url` and `issues_url` arrive on every event:
#: the first two from the `Context`, the last two from `META`.
CODES = {
    "ARG-ERR-TYPE-001": {
        "title": "Argument Type Error",
        "user_message": "Argument '{argname}' of '{caller}' has the wrong type. {detail}",
        "user_hint": "Check the type this argument expects. See {doc_url}.",
        "dev_message": "Type contract failed on {caller}({argname}=...): {detail}",
        "dev_hint": "Validate the type logic for '{argname}'.",
    },
    "ARG-ERR-VAL-001": {
        "title": "Argument Value Error",
        "user_message": "Argument '{argname}' of '{caller}' has an invalid value. {detail}",
        "user_hint": "Check the values this argument accepts. See {doc_url}.",
        "dev_message": "Value contract failed on {caller}({argname}=...): {detail}",
        "dev_hint": "Validate the value constraints for '{argname}'.",
    },
    "ARG-ERR-INV-001": {
        "title": "Argument Invariant Error",
        "user_message": "The arguments of '{caller}' are inconsistent with each other. {detail}",
        "user_hint": "Check how '{argname}' relates to the other arguments. See {doc_url}.",
        "dev_message": "Invariant failed on '{caller}' at '{argname}': {detail}",
        "dev_hint": "Check the inter-argument constraints.",
    },
    "ARG-ERR-MISS-001": {
        "title": "Argument Not Digested Error",
        "user_message": "Argument '{argname}' of '{caller}' could not be digested. {detail}",
        "user_hint": "This is an ArgDigest problem rather than yours. "
        "Please report it at {issues_url}.",
        "dev_message": "No digester for '{argname}' in '{caller}', or a cycle. {detail}",
        "dev_hint": "Implement the digester, or check the map for a cyclic dependency.",
    },
    "ARG-WARN-MISS-001": {
        "title": "Argument Not Digested Warning",
        "user_message": "No digester is registered for argument '{argname}' of '{caller}', "
        "so it was not validated.",
        "user_hint": "Define or register a digester for '{argname}'. See {doc_url}.",
        "dev_message": "Digestion skipped for '{argname}' in '{caller}'. {detail}",
        "dev_hint": "Register a digester, or remove '{argname}' from the map.",
    },
    "ARG-ERR-CONTRACT-001": {
        "title": "Unknown argument",
        "user_message": "'{caller}' does not accept the argument '{argname}'.",
        "user_hint": "Check the arguments it accepts.{guess} See {doc_url}.",
        "dev_message": "Argument '{argname}' is outside the declared contract of '{caller}'.",
        "dev_hint": "Extend the function contract if the argument is legitimate.{guess}",
    },
    "ARG-ERR-CONTRACT-002": {
        "title": "Missing required argument",
        "user_message": "The call to '{caller}' is incomplete. {detail}",
        "user_hint": "It carries none of the required arguments, so it cannot mean "
        "anything. See {doc_url}.",
        "dev_message": "Call to '{caller}' satisfies no required argument group. {detail}",
        "dev_hint": "Check 'requires_any_of' in the function contract.",
    },
    "ARG-ERR-CONTRACT-003": {
        "title": "Inconsistent arguments",
        "user_message": "The arguments given to '{caller}' cannot be used together. {detail}",
        "user_hint": "Pass the ones that belong together, and only those. See {doc_url}.",
        "dev_message": "Call to '{caller}' breaks an inter-argument rule. {detail}",
        "dev_hint": "Check 'mutually_exclusive' and 'co_required' in the function contract.",
    },
    "ARG-ERR-STD-001": {
        "title": "Standardizer broke its contract",
        "user_message": "The standardizer configured for '{caller}' misbehaved. {detail}",
        "user_hint": "This is a configuration problem in the library that registered it. "
        "See {doc_url}.",
        "dev_message": "The standardizer configured for '{caller}' broke its contract. {detail}",
        "dev_hint": "A standardizer takes (caller, kwargs) and must return the mapping; "
        "forgetting the return statement is the usual cause.",
    },
    "ARG-WARN-CONTRACT-001": {
        "title": "Function contract violation",
        "user_message": "The call to '{caller}' breaks its argument contract. {detail}",
        "user_hint": "It was reported instead of raised. See {doc_url}.",
        "dev_message": "Contract violation in '{caller}'. {detail}",
        "dev_hint": "The unknown_argument policy is set to 'warn' for this caller.",
    },
    "ARG-ERR-OPTDEP-001": {
        "title": "Optional dependency missing",
        "user_message": "'{caller}' needs the optional dependency '{dependency}', "
        "which is not installed.",
        "user_hint": "Install it with `pip install {distribution}`. If your library "
        "uses DepDigest, enable its '{dependency}' capability instead. "
        "Machine-readable: install_optional:{distribution}",
        "dev_message": "Optional dependency '{dependency}' absent at '{caller}'.",
        "dev_hint": "install_optional:{distribution}",
    },
    "ARG-WARN-TYPECHECK-001": {
        "title": "Type check skipped",
        "user_message": "Type checks are disabled because the optional dependency "
        "'beartype' is not available.",
        "user_hint": "Install 'beartype' to enable runtime type checking.",
        "dev_message": "type_check=True but 'beartype' is not installed, in '{caller}'.",
        "dev_hint": "Install beartype, or set type_check=False.",
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
