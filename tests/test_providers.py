"""Tests for provider implementations."""

import tempfile
from pathlib import Path

from src.providers.base import Command, ProviderConfig
from src.providers.claude import ClaudeProvider
from src.providers.codex import CodexProvider
from src.providers.gemini import GeminiProvider


class TestClaudeProvider:
  """Test Claude provider functionality."""

  def test_detect_existing_with_config(self):
    """Test detecting existing Claude config."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)
      (temp_path / 'CLAUDE.md').write_text('# Claude Config')

      provider = ClaudeProvider()
      assert provider.detect_existing(temp_path) is True

  def test_detect_existing_with_directory(self):
    """Test detecting existing Claude directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)
      (temp_path / '.claude').mkdir()

      provider = ClaudeProvider()
      assert provider.detect_existing(temp_path) is True

  def test_detect_existing_none(self):
    """Test detecting no existing Claude config."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      provider = ClaudeProvider()
      assert provider.detect_existing(temp_path) is False

  def test_get_existing_components(self):
    """Test getting existing component status."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      # Set up various components
      (temp_path / 'CLAUDE.md').write_text('# Config')
      commands_dir = temp_path / '.claude' / 'commands'
      commands_dir.mkdir(parents=True)
      (commands_dir / 'example.md').write_text('# Hello')
      (commands_dir / 'custom.md').write_text('# Custom')
      prompts_dir = temp_path / '.claude' / 'prompts'
      prompts_dir.mkdir(parents=True)
      (prompts_dir / 'test.md').write_text('# Test')
      (temp_path / 'agents.md').write_text('# Agents')

      provider = ClaudeProvider()
      status = provider.get_existing_components(temp_path)

      assert status['config'] is True
      assert status['commands'] == 2
      assert status['prompts'] == 0  # Claude Code doesn't have separate prompts
      assert status['agents'] is True

  def test_load_existing_config(self):
    """Test loading existing configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      # Set up configuration files
      (temp_path / 'CLAUDE.md').write_text('# Claude Configuration')
      commands_dir = temp_path / '.claude' / 'commands'
      commands_dir.mkdir(parents=True)
      (commands_dir / 'test.md').write_text(
        '---\ndescription: "Test command"\n---\n\n# Test Command\n\nTest content'
      )

      provider = ClaudeProvider()
      config = provider.load_existing_config(temp_path)

      assert config.main_config == '# Claude Configuration'
      assert len(config.commands) == 1
      assert config.commands[0].name == 'test'
      assert config.commands[0].description == 'Test command'

  def test_generate_config_minimal(self):
    """Test generating minimal configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      provider = ClaudeProvider()
      files = provider.generate_config(temp_path, ['config', 'commands'])

      assert 'CLAUDE.md' in files
      assert '.claude/commands/example.md' in files
      assert 'Project configured for Claude Code AI assistance' in files['CLAUDE.md']

  def test_generate_config_with_migration(self):
    """Test generating configuration with content migration."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      # Create base config with custom content
      base_config = ProviderConfig(
        main_config='# Custom Config',
        commands=[
          Command(name='custom', description='Custom command', content='# Custom\n\nCustom content')
        ],
        prompts=[
          Command(name='prompt', description='Test prompt', content='# Prompt\n\nPrompt content')
        ],
      )

      provider = ClaudeProvider()
      files = provider.generate_config(temp_path, ['config', 'commands', 'prompts'], base_config)

      assert files['CLAUDE.md'] == '# Custom Config'
      assert '.claude/commands/custom.md' in files
      assert '.claude/commands/prompt.md' in files  # Prompts stored as commands in Claude
      assert files['.claude/commands/custom.md'] == '# Custom\n\nCustom content'


class TestGeminiProvider:
  """Test Gemini provider functionality."""

  def test_detect_existing(self):
    """Test detecting existing Gemini config."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)
      (temp_path / 'GEMINI.md').write_text('# Gemini Config')

      provider = GeminiProvider()
      assert provider.detect_existing(temp_path) is True

  def test_generate_config(self):
    """Test generating Gemini configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      provider = GeminiProvider()
      files = provider.generate_config(temp_path, ['config', 'commands'])

      assert 'GEMINI.md' in files
      assert '.gemini/commands/example.toml' in files

  def test_convert_command_from_claude(self):
    """Test converting command from Claude format to Gemini TOML."""
    provider = GeminiProvider()

    claude_command = Command(
      name='test',
      description='Test command',
      content='---\ndescription: "Test"\n---\n\n# Test Command\n\nContent',
    )

    converted = provider._convert_command_to_gemini_toml(claude_command)

    # Should convert to TOML format
    assert 'description = "Test command"' in converted
    assert 'prompt = """' in converted
    assert '# Test Command' in converted
    assert 'Content' in converted


class TestCodexProvider:
  """Test Codex provider functionality."""

  def test_detect_existing(self):
    """Test detecting existing Codex config."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)
      (temp_path / 'AGENTS.md').write_text('# Project Instructions')

      provider = CodexProvider()
      assert provider.detect_existing(temp_path) is True

  def test_generate_config(self):
    """Test generating Codex configuration."""
    with tempfile.TemporaryDirectory() as temp_dir:
      temp_path = Path(temp_dir)

      provider = CodexProvider()
      files = provider.generate_config(temp_path, ['config', 'commands'])

      assert 'AGENTS.md' in files
      assert '.codex/prompts/example.md' in files
      assert '~/.codex/prompts' in files['AGENTS.md']
      assert 'Copy this file to `~/.codex/prompts/example.md`' in files['.codex/prompts/example.md']
