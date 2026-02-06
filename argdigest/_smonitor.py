PROFILE = "user"

SMONITOR = {
    "level": "WARNING",
    "trace_depth": 3,
    "capture_warnings": False,
    "capture_logging": True,
    "theme": "plain",
}

PROFILES = {
    "user": {
        "level": "WARNING",
    },
    "dev": {
        "level": "INFO",
        "show_traceback": True,
    },
    "qa": {
        "level": "INFO",
        "show_traceback": True,
    },
    "agent": {
        "level": "WARNING",
    },
    "debug": {
        "level": "DEBUG",
        "show_traceback": True,
    },
}

CODES = {
    "ARGDIGEST-MISSING-DIGESTER": {
        "title": "Missing digester",
        "user_message": "No hay digester para '{argname}'.",
        "user_hint": "Define un digester para '{argname}' o desactiva la digestion.",
        "dev_message": "No digester for argument '{argname}'.",
        "dev_hint": "Register a digester for '{argname}' or adjust rules.",
        "qa_message": "No digester for argument '{argname}'.",
        "qa_hint": "Register a digester for '{argname}'.",
        "agent_message": "No digester for argument '{argname}'.",
        "agent_hint": "Register a digester for '{argname}'.",
    },
    "ARGDIGEST-TYPECHECK-SKIP": {
        "title": "Type check skipped",
        "user_message": "El chequeo de tipos fue omitido.",
        "user_hint": "Instala 'beartype' para habilitar type_check.",
        "dev_message": "type_check=True but 'beartype' is not installed. Skipping.",
        "dev_hint": "Install beartype to enable type checking.",
        "qa_message": "type_check=True but 'beartype' is not installed. Skipping.",
        "qa_hint": "Install beartype to enable type checking.",
        "agent_message": "type_check=True but 'beartype' is not installed. Skipping.",
        "agent_hint": "Install beartype to enable type checking.",
    },
}

SIGNALS = {
    "argdigest.digester": {
        "extra_required": ["argname"],
    }
}
