import pytest
import os
from argdigest.cli import main
from argdigest.core.agent_docs import generate_agent_docs

def test_agent_docs_generation(tmp_path):
    # We can use 'packlib' if we add examples to path, or just mock it.
    # For now, let's test the logic with a module we know exists.
    output_file = tmp_path / "AGENT_TEST.md"
    path = generate_agent_docs("argdigest", output_file=str(output_file))
    
    assert os.path.exists(path)
    with open(path, "r") as f:
        content = f.read()
        assert "# ArgDigest Agent Instructions for argdigest" in content
        assert "## 1. Project Context" in content
        assert "argdigest agent update" in content

def test_cli_agent_init_help(capsys):
    # Test that the CLI parser works for the agent command
    with pytest.raises(SystemExit):
        with pytest.MonkeyPatch().context() as m:
            m.setattr("sys.argv", ["argdigest", "agent", "--help"])
            main()
    
    out, _ = capsys.readouterr()
    assert "Agent sub-commands" in out

def test_cli_agent_init_real(capsys):
    # Test real execution of agent init
    with pytest.MonkeyPatch().context() as m:
        # Use argdigest as the module to audit
        m.setattr("sys.argv", ["argdigest", "agent", "init", "--module", "argdigest"])
        main()
    out, _ = capsys.readouterr()
    assert "Initialized agent instructions" in out
    assert os.path.exists("ARG_DIGEST_AGENTS.md")
    os.remove("ARG_DIGEST_AGENTS.md")

def test_agent_docs_error():
    from argdigest.core.agent_docs import generate_agent_docs
    with pytest.raises(ImportError, match="Could not import module"):
        generate_agent_docs("non_existent_package_123")

def test_cli_audit_command(capsys):
    # Test the audit command on argdigest itself
    with pytest.MonkeyPatch().context() as m:
        m.setattr("sys.argv", ["argdigest", "audit", "argdigest"])
        main()
    
    out, _ = capsys.readouterr()
    assert "Audit Report for module: argdigest" in out

def test_cli_agent_update(capsys):
    with pytest.MonkeyPatch().context() as m:
        m.setattr("sys.argv", ["argdigest", "agent", "update", "--module", "argdigest"])
        main()
    out, _ = capsys.readouterr()
    assert "Updated agent instructions" in out
