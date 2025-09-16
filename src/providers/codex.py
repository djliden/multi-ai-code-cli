"""OpenAI Codex provider implementation."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import Command, Provider, ProviderConfig


class CodexProvider(Provider):
  """OpenAI Codex provider for managing .codex/ configurations."""

  @property
  def name(self) -> str:
    """Provider name."""
    return 'codex'

  @property
  def config_files(self) -> List[str]:
    """Main configuration files."""
    return ['AGENTS.md']

  @property
  def directories(self) -> List[str]:
    """Required directories."""
    return ['.codex/prompts']

  def detect_existing(self, project_dir: Path) -> bool:
    """Check if Codex is already configured."""
    agents_md = project_dir / 'AGENTS.md'
    codex_dir = project_dir / '.codex'
    return agents_md.exists() or codex_dir.exists()

  def get_existing_components(self, project_dir: Path) -> Dict[str, Any]:
    """Get status of existing Codex components."""
    status = {
      'config': (project_dir / 'AGENTS.md').exists(),
      'commands': 0,  # Codex doesn't have commands directory
      'prompts': 0,
      'agents': (project_dir / 'AGENTS.md').exists(),  # Same file as config
    }

    # Count existing prompts
    prompts_dir = project_dir / '.codex' / 'prompts'
    if prompts_dir.exists():
      status['prompts'] = len(list(prompts_dir.glob('*.md')))

    return status

  def load_existing_config(self, project_dir: Path) -> ProviderConfig:
    """Load existing Codex configuration and content."""
    config = ProviderConfig()

    # Load main AGENTS.md
    agents_md = project_dir / 'AGENTS.md'
    if agents_md.exists():
      config.main_config = agents_md.read_text()
      config.agents = agents_md.read_text()  # Same file serves as both config and agents

    # Codex doesn't have commands directory - only prompts

    # Load prompts from .codex/prompts/
    prompts_dir = project_dir / '.codex' / 'prompts'
    if prompts_dir.exists():
      for prompt_file in prompts_dir.glob('*.md'):
        content = prompt_file.read_text()
        description = self._extract_description(content)
        config.prompts.append(
          Command(name=prompt_file.stem, description=description, content=content)
        )

    return config

  def generate_config(
    self,
    project_dir: Path,
    components: List[str] = None,
    base_config: Optional[ProviderConfig] = None,
  ) -> Dict[str, str]:
    """Generate Codex configuration files for specified components."""
    if components is None:
      components = ['config', 'commands']

    files = {}

    # Generate main AGENTS.md
    if 'config' in components:
      if base_config and base_config.main_config:
        files['AGENTS.md'] = base_config.main_config
      elif base_config and base_config.agents:
        files['AGENTS.md'] = base_config.agents
      else:
        files['AGENTS.md'] = (
          '# OpenAI Codex Project Notes\n\n'
          'Codex only loads custom prompts from the global `$CODEX_HOME/prompts/` directory '
          '(typically `~/.codex/prompts`). '
          'Prompts kept in this repository are templates you can copy '
          'or symlink into that global folder when you want them available as slash commands.\n\n'
          '## Using project prompts\n'
          '1. Review prompts under `.codex/prompts/` in this project.\n'
          '2. Copy or symlink any prompt into `~/.codex/prompts/`.\n'
          '3. Restart your Codex session so the slash command list refreshes.\n\n'
          'Tip: keep the project versions editable here, then sync updates to your '
          'global Codex prompts.\n'
        )

    # Generate prompt files (Codex commands are stored as prompts)
    if 'commands' in components:
      if base_config and base_config.commands:
        for command in base_config.commands:
          files[f'.codex/prompts/{command.name}.md'] = self._convert_command_to_codex(command)
      else:
        # Example prompt template when no commands to migrate
        files['.codex/prompts/example.md'] = (
          '# Example Prompt\n\n'
          'Copy this file to `~/.codex/prompts/example.md` so Codex can load it as a slash '
          'command.\n\n'
          'You can safely keep editing the project version and resync it to your global Codex '
          'prompt directory when changes are ready.\n'
        )

    # Generate prompt files
    if 'prompts' in components:
      if base_config and base_config.prompts:
        for prompt in base_config.prompts:
          files[f'.codex/prompts/{prompt.name}.md'] = prompt.content
      # Don't create duplicate example if commands already created one

    return files

  def get_editor_files(self, project_dir: Path, components: List[str] = None) -> List[str]:
    """Files to open in editor after generation for specified components."""
    if components is None or 'config' in components:
      return ['AGENTS.md']
    return []

  def _convert_command_to_codex(self, command: Command) -> str:
    """Convert a command from another provider to Codex format."""
    # Remove Claude-specific frontmatter and adapt for Codex
    content = command.content

    # Remove frontmatter if present
    if content.startswith('---'):
      parts = content.split('---', 2)
      if len(parts) >= 3:
        content = parts[2].strip()

    # Simple conversion - just use the content
    return content

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
