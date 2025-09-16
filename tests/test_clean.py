"""Tests for the clean command."""

from .conftest import run_cli_command, temp_project_dir


def test_clean_specific_provider():
  """Test cleaning specific provider."""
  with temp_project_dir() as temp_path:
    # Set up multiple providers
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'example.md').write_text('# Hello')

    gemini_config_dir = temp_path / '.gemini'
    gemini_config_dir.mkdir()
    (gemini_config_dir / 'config').write_text('# Gemini Config')

    result = run_cli_command(['clean', 'claude', '--force'])

    assert result.exit_code == 0
    assert 'Removed' in result.stdout

    # Claude should be removed, Gemini should remain
    assert not (temp_path / 'CLAUDE.md').exists()
    assert not (temp_path / '.claude').exists()
    assert (temp_path / '.gemini' / 'config').exists()


def test_clean_specific_components():
  """Test cleaning specific components only."""
  with temp_project_dir() as temp_path:
    # Set up Claude with all components
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'example.md').write_text('# Hello')
    prompts_dir = temp_path / '.claude' / 'prompts'
    prompts_dir.mkdir(parents=True)
    (prompts_dir / 'test.md').write_text('# Test')
    (temp_path / 'agents.md').write_text('# Agents')

    result = run_cli_command(['clean', 'claude', '--commands', '--force'])

    assert result.exit_code == 0

    # Only commands should be removed
    assert (temp_path / 'CLAUDE.md').exists()
    assert not (temp_path / '.claude' / 'commands').exists()
    assert (temp_path / '.claude' / 'prompts').exists()
    assert (temp_path / 'agents.md').exists()


def test_clean_all_providers():
  """Test cleaning all providers."""
  with temp_project_dir() as temp_path:
    # Set up multiple providers
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'example.md').write_text('# Hello')

    gemini_config_dir = temp_path / '.gemini'
    gemini_config_dir.mkdir()
    (gemini_config_dir / 'config').write_text('# Gemini Config')

    codex_config_dir = temp_path / '.codex'
    codex_config_dir.mkdir()
    (codex_config_dir / 'config').write_text('# Codex Config')

    result = run_cli_command(['clean', 'all', '--force'])

    assert result.exit_code == 0
    assert 'All providers removed' in result.stdout

    # All providers should be removed
    assert not (temp_path / 'CLAUDE.md').exists()
    assert not (temp_path / '.claude').exists()
    assert not (temp_path / '.gemini').exists()
    assert not (temp_path / '.codex').exists()


def test_clean_nonexistent_provider():
  """Test cleaning non-existent provider."""
  with temp_project_dir():
    result = run_cli_command(['clean', 'claude', '--force'])

    assert result.exit_code == 0
    assert 'claude is not configured' in result.stdout


def test_clean_empty_project():
  """Test cleaning in empty project."""
  with temp_project_dir():
    result = run_cli_command(['clean', 'all', '--force'])

    assert result.exit_code == 0  # Should handle gracefully
