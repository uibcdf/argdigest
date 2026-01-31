def digest_selection(selection, syntax="MolSysMT", caller=None):
    # Mimics MolSysMT logic: relies on 'syntax' being injected
    return f"Selection: {selection}, Syntax: {syntax}"
