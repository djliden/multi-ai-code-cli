"""Tests for the list command."""

from .conftest import run_cli_command, temp_project_dir


def test_list_empty_project():
  """Test list command on empty project."""
  with temp_project_dir():
    result = run_cli_command(['list'])

    assert result.exit_code == 0
    assert 'AI Provider Configuration Status' in result.stdout
    assert 'No AI providers configured' in result.stdout


def test_list_with_providers():
  """Test list command with configured providers."""
  with temp_project_dir() as temp_path:
    # Set up providers
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'example.md').write_text('# Hello')
    (commands_dir / 'custom.md').write_text('# Custom')

    # Claude doesn't have separate prompts directory according to docs
    (temp_path / 'agents.md').write_text('# Agents')

    # Gemini uses GEMINI.md and .toml files in .gemini/commands/
    (temp_path / 'GEMINI.md').write_text('# Gemini Config')
    gemini_commands_dir = temp_path / '.gemini' / 'commands'
    gemini_commands_dir.mkdir(parents=True)
    (gemini_commands_dir / 'test.toml').write_text('description = "Test"\nprompt = "Test command"')

    result = run_cli_command(['list'])

    assert result.exit_code == 0
    assert '✓ (2)' in result.stdout  # 2 commands for Claude
    assert '✓ (1)' in result.stdout  # 1 command for Gemini (.toml file)
    # Claude doesn't have separate prompts, so it should show ✗ for prompts
    assert 'Configured providers: claude, gemini' in result.stdout


def test_list_partial_configuration():
  """Test list command with partial provider configuration."""
  with temp_project_dir() as temp_path:
    # Only config file, no commands
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')

    result = run_cli_command(['list'])

    assert result.exit_code == 0
    assert '✓' in result.stdout  # config exists
    assert '✗' in result.stdout  # commands/prompts don't exist
