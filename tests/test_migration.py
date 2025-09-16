"""Tests for content migration functionality."""

import tempfile
from pathlib import Path

from src.core.generator import ConfigGenerator


def test_migration_claude_to_gemini():
  """Test migrating content from Claude to Gemini."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Set up Claude provider with custom content
    (temp_path / 'CLAUDE.md').write_text('# Claude Configuration\n\nCustom config content')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'custom.md').write_text(
      '---\ndescription: "Custom command"\n---\n\n# Custom Command\n\nCustom functionality'
    )
    (commands_dir / 'deploy.md').write_text('# Deploy Command\n\nDeploy the application')

    # Claude doesn't have a separate prompts directory according to docs
    # All commands/prompts go in .claude/commands/
    (commands_dir / 'review.md').write_text('# Code Review Prompt\n\nReview this code for quality')

    (temp_path / 'agents.md').write_text('# AI Agents\n\nAgent configurations')

    # Migrate to Gemini
    generator = ConfigGenerator()
    files = generator.generate_provider_config(
      project_dir=temp_path,
      provider_name='gemini',
      components=['config', 'commands', 'prompts'],
      migrate_from=['claude'],
    )

    # Verify migration - Gemini uses GEMINI.md and .toml files according to docs
    assert 'GEMINI.md' in files
    assert '.gemini/commands/custom.toml' in files
    assert '.gemini/commands/deploy.toml' in files
    assert (
      '.gemini/commands/review.toml' in files
    )  # Should migrate Claude commands to Gemini commands

    # Verify content transformation (should be in TOML format)
    custom_content = files['.gemini/commands/custom.toml']
    assert 'description = "Custom command"' in custom_content
    assert 'prompt = """' in custom_content
    assert '# Custom Command' in custom_content
    assert 'Custom functionality' in custom_content


def test_migration_multiple_sources():
  """Test migrating content from multiple source providers."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Set up Claude provider
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    claude_commands = temp_path / '.claude' / 'commands'
    claude_commands.mkdir(parents=True)
    (claude_commands / 'claude_cmd.md').write_text('# Claude Command')

    # Set up Gemini provider
    (temp_path / 'GEMINI.md').write_text('# Gemini Config')
    gemini_dir = temp_path / '.gemini'
    gemini_commands = gemini_dir / 'commands'
    gemini_commands.mkdir(parents=True)
    (gemini_commands / 'gemini_cmd.toml').write_text(
      'description = "Gemini Command"\nprompt = "Gemini command content"'
    )

    # Migrate from both to Codex (commands become prompts)
    generator = ConfigGenerator()
    files = generator.generate_provider_config(
      project_dir=temp_path,
      provider_name='codex',
      components=['commands'],
      migrate_from=['claude', 'gemini'],
    )

    # Should have prompts from both sources (commands migrated to prompts)
    assert '.codex/prompts/claude_cmd.md' in files
    assert '.codex/prompts/gemini_cmd.md' in files


def test_migration_partial_content():
  """Test migrating when source has partial content."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Set up Claude with only config and commands (no prompts)
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'test.md').write_text('# Test Command')

    # Migrate to Gemini requesting all components
    generator = ConfigGenerator()
    files = generator.generate_provider_config(
      project_dir=temp_path,
      provider_name='gemini',
      components=['config', 'commands', 'prompts'],
      migrate_from=['claude'],
    )

    # Should have config and commands migrated, but no prompts created
    assert 'GEMINI.md' in files
    assert '.gemini/commands/test.toml' in files
    # No prompt files should be generated since source doesn't have any
    prompt_files = [f for f in files.keys() if '/prompts/' in f]
    assert len(prompt_files) == 0


def test_migration_round_trip():
  """Test round-trip migration preserves content."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Set up original content
    original_config = '# Original Configuration\n\nThis is original content'
    original_command = '# Original Command\n\nOriginal command content'

    (temp_path / 'CLAUDE.md').write_text(original_config)
    commands_dir = temp_path / '.claude' / 'commands'
    commands_dir.mkdir(parents=True)
    (commands_dir / 'original.md').write_text(
      '---\ndescription: "Original"\n---\n\n' + original_command
    )

    generator = ConfigGenerator()

    # Migrate Claude -> Gemini
    files = generator.generate_provider_config(
      project_dir=temp_path,
      provider_name='gemini',
      components=['config', 'commands'],
      migrate_from=['claude'],
    )

    # Write Gemini files
    generator.write_config_files(temp_path, files)

    # Migrate Gemini -> Codex
    files = generator.generate_provider_config(
      project_dir=temp_path,
      provider_name='codex',
      components=['config', 'commands'],
      migrate_from=['gemini'],
    )

    # Verify content preservation
    assert files['AGENTS.md'] == original_config
    # Command content should preserve main content (commands migrated to prompts)
    assert '# Original Command' in files['.codex/prompts/original.md']
    assert 'Original command content' in files['.codex/prompts/original.md']


def test_migration_no_sources():
  """Test generating config when no migration sources exist."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    generator = ConfigGenerator()
    files = generator.generate_provider_config(
      project_dir=temp_path,
      provider_name='claude',
      components=['config', 'commands'],
      migrate_from=['gemini', 'codex'],  # These don't exist
    )

    # Should fall back to default templates
    assert 'CLAUDE.md' in files
    assert '.claude/commands/example.md' in files
    assert 'Project configured for Claude Code AI assistance' in files['CLAUDE.md']


def test_merge_source_configs():
  """Test merging configurations from multiple sources."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)

    # Source 1: Claude with config and commands
    (temp_path / 'CLAUDE.md').write_text('# Claude Config')
    claude_commands = temp_path / '.claude' / 'commands'
    claude_commands.mkdir(parents=True)
    (claude_commands / 'cmd1.md').write_text('# Command 1')

    # Source 2: Gemini with commands and prompts
    (temp_path / 'GEMINI.md').write_text('# Gemini Config')
    gemini_dir = temp_path / '.gemini'
    gemini_commands = gemini_dir / 'commands'
    gemini_commands.mkdir(parents=True)
    (gemini_commands / 'cmd2.toml').write_text(
      'description = "Command 2"\nprompt = "Command 2 content"'
    )

    generator = ConfigGenerator()
    merged_config = generator._merge_source_configs(temp_path, ['claude', 'gemini'])

    # Should have main config from first source
    assert merged_config.main_config == '# Claude Config'

    # Should have commands from both sources
    assert len(merged_config.commands) == 2
    command_names = [cmd.name for cmd in merged_config.commands]
    assert 'cmd1' in command_names
    assert 'cmd2' in command_names

    # Gemini doesn't have prompts directory anymore, so no prompts should be found
    assert len(merged_config.prompts) == 0
