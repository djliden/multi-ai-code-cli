"""Gemini CLI provider implementation."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import Command, Provider, ProviderConfig


class GeminiProvider(Provider):
  """Gemini CLI provider for managing .gemini/ configurations."""

  @property
  def name(self) -> str:
    """Provider name."""
    return 'gemini'

  @property
  def config_files(self) -> List[str]:
    """Main configuration files."""
    return ['GEMINI.md']

  @property
  def directories(self) -> List[str]:
    """Required directories."""
    return ['.gemini/commands']

  def detect_existing(self, project_dir: Path) -> bool:
    """Check if Gemini CLI is already configured."""
    gemini_md = project_dir / 'GEMINI.md'
    gemini_dir = project_dir / '.gemini'
    return gemini_md.exists() or gemini_dir.exists()

  def get_existing_components(self, project_dir: Path) -> Dict[str, Any]:
    """Get status of existing Gemini components."""
    status = {
      'config': (project_dir / 'GEMINI.md').exists(),
      'commands': 0,
      'prompts': 0,
      'agents': False,  # Gemini doesn't use agents.md by default
    }

    # Count existing commands (.toml files)
    commands_dir = project_dir / '.gemini' / 'commands'
    if commands_dir.exists():
      status['commands'] = len(list(commands_dir.glob('*.toml')))

    # Gemini doesn't have separate prompts directory

    return status

  def load_existing_config(self, project_dir: Path) -> ProviderConfig:
    """Load existing Gemini configuration and content."""
    config = ProviderConfig()

    # Load main GEMINI.md
    gemini_md = project_dir / 'GEMINI.md'
    if gemini_md.exists():
      config.main_config = gemini_md.read_text()

    # Load commands from .gemini/commands/ (.toml files)
    commands_dir = project_dir / '.gemini' / 'commands'
    if commands_dir.exists():
      for cmd_file in commands_dir.glob('*.toml'):
        content = cmd_file.read_text()
        description = self._extract_description_from_toml(content)
        config.commands.append(
          Command(name=cmd_file.stem, description=description, content=content)
        )

    # Gemini doesn't have separate prompts directory

    return config

  def generate_config(
    self,
    project_dir: Path,
    components: List[str] = None,
    base_config: Optional[ProviderConfig] = None,
  ) -> Dict[str, str]:
    """Generate Gemini CLI configuration files for specified components."""
    if components is None:
      components = ['config', 'commands']

    files = {}

    # Generate main GEMINI.md
    if 'config' in components:
      if base_config and base_config.main_config:
        files['GEMINI.md'] = base_config.main_config
      else:
        files['GEMINI.md'] = (
          '# Gemini CLI Configuration\n\nProject configured for Gemini CLI assistance.\n'
        )

    # Generate command files (.toml format)
    if 'commands' in components:
      if base_config and base_config.commands:
        for command in base_config.commands:
          files[f'.gemini/commands/{command.name}.toml'] = self._convert_command_to_gemini_toml(
            command
          )
      else:
        # Example command template
        files['.gemini/commands/example.toml'] = (
          'description = "Example command"\n' 'prompt = "This is an example command template"\n'
        )

    # Gemini doesn't have separate prompts - they would be commands

    return files

  def get_editor_files(self, project_dir: Path, components: List[str] = None) -> List[str]:
    """Files to open in editor after generation for specified components."""
    if components is None or 'config' in components:
      return ['GEMINI.md']
    return []

  def _convert_command_to_gemini_toml(self, command: Command) -> str:
    """Convert a command from another provider to Gemini TOML format."""
    # Extract content without frontmatter
    content = command.content

    # Remove frontmatter if present
    if content.startswith('---'):
      parts = content.split('---', 2)
      if len(parts) >= 3:
        content = parts[2].strip()

    # Convert to TOML format
    description = command.description or 'Migrated command'
    return f'description = "{description}"\nprompt = """{content}"""'

  def _extract_description_from_toml(self, content: str) -> str:
    """Extract description from TOML content."""
    lines = content.strip().split('\n')
    for line in lines:
      line = line.strip()
      if line.startswith('description = '):
        # Extract value from TOML line
        value = line.split('description = ', 1)[1]
        # Remove quotes
        return value.strip('"\'')
    return ''

  def _extract_description(self, content: str) -> str:
    """Extract description from markdown content."""
    lines = content.strip().split('\n')
    for line in lines:
      line = line.strip()
      if line and not line.startswith('---'):
        if line.startswith('#'):
          return line.lstrip('#').strip()
        return line
    return ''
