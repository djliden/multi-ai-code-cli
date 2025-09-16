"""Claude Code provider implementation."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import Command, Provider, ProviderConfig


class ClaudeProvider(Provider):
  """Claude Code provider for managing .claude/ configurations."""

  @property
  def name(self) -> str:
    """Provider name."""
    return 'claude'

  @property
  def config_files(self) -> List[str]:
    """Main configuration files."""
    return ['CLAUDE.md']

  @property
  def directories(self) -> List[str]:
    """Required directories."""
    return ['.claude/commands']

  def detect_existing(self, project_dir: Path) -> bool:
    """Check if Claude Code is already configured."""
    claude_md = project_dir / 'CLAUDE.md'
    claude_dir = project_dir / '.claude'
    return claude_md.exists() or claude_dir.exists()

  def get_existing_components(self, project_dir: Path) -> Dict[str, Any]:
    """Get status of existing Claude components."""
    status = {
      'config': (project_dir / 'CLAUDE.md').exists(),
      'commands': 0,
      'prompts': 0,
      'agents': (project_dir / 'agents.md').exists(),
    }

    # Count existing commands
    commands_dir = project_dir / '.claude' / 'commands'
    if commands_dir.exists():
      status['commands'] = len(list(commands_dir.glob('*.md')))

    # For Claude Code, prompts are just commands in .claude/commands/
    # No separate prompts count needed - they're included in commands count

    return status

  def load_existing_config(self, project_dir: Path) -> ProviderConfig:
    """Load existing Claude configuration and content."""
    config = ProviderConfig()

    # Load main CLAUDE.md config
    claude_md = project_dir / 'CLAUDE.md'
    if claude_md.exists():
      config.main_config = claude_md.read_text()

    # Load commands from .claude/commands/
    commands_dir = project_dir / '.claude' / 'commands'
    if commands_dir.exists():
      for cmd_file in commands_dir.glob('*.md'):
        content = cmd_file.read_text()
        description = self._extract_description(content)
        config.commands.append(
          Command(name=cmd_file.stem, description=description, content=content)
        )

    # For Claude Code, prompts are just commands in .claude/commands/
    # No separate prompts directory

    # Check for agents.md
    agents_file = project_dir / 'agents.md'
    if agents_file.exists():
      config.agents = agents_file.read_text()

    return config

  def generate_config(
    self,
    project_dir: Path,
    components: List[str] = None,
    base_config: Optional[ProviderConfig] = None,
  ) -> Dict[str, str]:
    """Generate Claude Code configuration files for specified components."""
    if components is None:
      components = ['config', 'commands']

    files = {}

    # Generate main CLAUDE.md
    if 'config' in components:
      if base_config and base_config.main_config:
        files['CLAUDE.md'] = base_config.main_config
      else:
        files['CLAUDE.md'] = (
          '# Claude Code Configuration\n\nProject configured for Claude Code AI assistance.\n'
        )

    # Generate command files
    if 'commands' in components:
      if base_config and base_config.commands:
        for command in base_config.commands:
          files[f'.claude/commands/{command.name}.md'] = command.content
      else:
        # Example command template
        files['.claude/commands/example.md'] = (
          '---\ndescription: "Example command"\n---\n\n'
          '# Example Command\n\nThis is an example command template.\n'
        )

    # Generate prompt files - for Claude Code, prompts are stored as commands
    if 'prompts' in components and base_config and base_config.prompts:
      for prompt in base_config.prompts:
        files[f'.claude/commands/{prompt.name}.md'] = prompt.content

    # Generate agents.md
    if 'agents' in components and base_config and base_config.agents:
      files['agents.md'] = base_config.agents

    return files

  def get_editor_files(self, project_dir: Path, components: List[str] = None) -> List[str]:
    """Files to open in editor after generation for specified components."""
    if components is None or 'config' in components:
      return ['CLAUDE.md']
    return []

  def _extract_description(self, content: str) -> str:
    """Extract description from markdown frontmatter or first line."""
    # Try to extract from frontmatter
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
      frontmatter = frontmatter_match.group(1)
      desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
      if desc_match:
        return desc_match.group(1)

    # Fall back to first non-empty line or header
    lines = content.strip().split('\n')
    for line in lines:
      line = line.strip()
      if line and not line.startswith('---'):
        if line.startswith('#'):
          return line.lstrip('#').strip()
        return line

    return ''
