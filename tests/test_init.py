"""Tests for the init command."""

from .conftest import run_cli_command, temp_project_dir


def test_init_claude_basic():
  """Test basic Claude initialization."""
  with temp_project_dir() as temp_path:
    result = run_cli_command(['init', '--claude'])

    assert result.exit_code == 0
    assert 'Initializing claude' in result.stdout
    assert 'Created 2 files' in result.stdout
    assert (temp_path / 'CLAUDE.md').exists()
    assert (temp_path / '.claude' / 'commands' / 'example.md').exists()


def test_init_all_providers():
  """Test initializing all providers."""
  with temp_project_dir() as temp_path:
    result = run_cli_command(['init', '--claude', '--gemini', '--codex'])

    assert result.exit_code == 0
    assert 'Initializing claude' in result.stdout
    assert 'Initializing gemini' in result.stdout
    assert 'Initializing codex' in result.stdout

    # Check all provider files exist
    assert (temp_path / 'CLAUDE.md').exists()
    assert (temp_path / '.claude' / 'commands' / 'example.md').exists()
    assert (temp_path / 'GEMINI.md').exists()
    assert (temp_path / '.gemini' / 'commands' / 'example.toml').exists()
    assert (temp_path / 'AGENTS.md').exists()
    assert (temp_path / '.codex' / 'prompts' / 'example.md').exists()


def test_init_config_only():
  """Test initializing only config components."""
  with temp_project_dir() as temp_path:
    result = run_cli_command(['init', '--claude', '--config'])

    assert result.exit_code == 0
    assert (temp_path / 'CLAUDE.md').exists()
    assert not (temp_path / '.claude' / 'commands').exists()


def test_init_commands_only():
  """Test initializing only command components."""
  with temp_project_dir() as temp_path:
    result = run_cli_command(['init', '--gemini', '--commands'])

    assert result.exit_code == 0
    assert (temp_path / '.gemini' / 'commands' / 'example.toml').exists()
    assert not (temp_path / 'GEMINI.md').exists()


def test_init_force_overwrite():
  """Test force overwriting existing files."""
  with temp_project_dir() as temp_path:
    # Create initial file
    claude_file = temp_path / 'CLAUDE.md'
    claude_file.parent.mkdir(parents=True, exist_ok=True)
    claude_file.write_text('Original content')

    # Without force - should not overwrite existing file but can create new ones
    result = run_cli_command(['init', '--claude'])
    assert result.exit_code == 0
    # Should create commands but not overwrite existing CLAUDE.md
    assert claude_file.read_text() == 'Original content'
    assert (temp_path / '.claude' / 'commands' / 'example.md').exists()

    # With force - should overwrite
    result = run_cli_command(['init', '--claude', '--force'])
    assert result.exit_code == 0
    assert 'Created' in result.stdout
    assert claude_file.read_text() != 'Original content'
