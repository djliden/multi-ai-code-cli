"""Tests for the add command."""

from .conftest import run_cli_command, temp_project_dir


def test_add_to_empty_project():
  """Test adding provider to empty project."""
  with temp_project_dir() as temp_path:
    result = run_cli_command(['add', 'claude'])

    assert result.exit_code == 0
    assert 'Adding claude' in result.stdout
    assert (temp_path / 'CLAUDE.md').exists()
    assert (temp_path / '.claude' / 'commands' / 'example.md').exists()


def test_add_with_migration():
  """Test adding provider with content migration."""
  with temp_project_dir() as temp_path:
    # Set up initial Claude provider with custom content
    (temp_path / 'CLAUDE.md').write_text('# Claude Config\n\nCustom config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'custom.md').write_text('# Custom Command\n\nTest command')

    result = run_cli_command(['add', 'gemini', '--migrate'])

    assert result.exit_code == 0
    assert 'Migrating content from: claude' in result.stdout

    # Check migration worked - Gemini uses GEMINI.md
    assert (temp_path / 'GEMINI.md').exists()
    assert (temp_path / '.gemini' / 'commands' / 'custom.toml').exists()

    # Verify content was migrated
    migrated_command = (temp_path / '.gemini' / 'commands' / 'custom.toml').read_text()
    assert 'Custom Command' in migrated_command


def test_add_specific_components():
  """Test adding specific components only."""
  with temp_project_dir() as temp_path:
    # Initialize with config only
    result = run_cli_command(['add', 'claude', '--config'])
    assert result.exit_code == 0
    assert (temp_path / 'CLAUDE.md').exists()
    assert not (temp_path / '.claude' / 'commands').exists()

    # Add commands
    result = run_cli_command(['add', 'claude', '--commands'])
    assert result.exit_code == 0
    assert (temp_path / '.claude' / 'commands' / 'example.md').exists()


def test_add_invalid_provider():
  """Test adding invalid provider."""
  with temp_project_dir():
    result = run_cli_command(['add', 'invalid'])

    assert result.exit_code == 1
    assert 'Unknown provider: invalid' in result.stdout
    assert 'Available providers:' in result.stdout


def test_add_without_migration():
  """Test adding provider without migration."""
  with temp_project_dir() as temp_path:
    # Set up initial Claude provider
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'custom.md').write_text('# Custom Command')

    result = run_cli_command(['add', 'gemini', '--no-migrate'])

    assert result.exit_code == 0
    assert 'Migrating content from' not in result.stdout

    # Check only default content was created
    gemini_commands = temp_path / '.gemini' / 'commands'
    if gemini_commands.exists():
      # Should only have example.toml, not custom.toml
      command_files = list(gemini_commands.glob('*.toml'))
      assert len(command_files) == 1
      assert command_files[0].name == 'example.toml'
