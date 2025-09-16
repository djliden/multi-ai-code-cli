"""Core detection logic for AI provider configurations."""

from pathlib import Path
from typing import Any, Dict, List

from ..providers.base import Provider
from ..providers.claude import ClaudeProvider
from ..providers.codex import CodexProvider
from ..providers.gemini import GeminiProvider


class ProjectDetector:
  """Detect existing AI provider configurations in a project."""

  def __init__(self):
    self.providers = {
      'claude': ClaudeProvider(),
      'gemini': GeminiProvider(),
      'codex': CodexProvider(),
    }

  def get_provider(self, name: str) -> Provider:
    """Get provider by name."""
    return self.providers.get(name)

  def get_all_providers(self) -> Dict[str, Provider]:
    """Get all available providers."""
    return self.providers.copy()

  def detect_existing_providers(self, project_dir: Path) -> Dict[str, bool]:
    """Detect which providers are already configured."""
    return {
      name: provider.detect_existing(project_dir) for name, provider in self.providers.items()
    }

  def get_provider_status(self, project_dir: Path) -> Dict[str, Dict[str, Any]]:
    """Get detailed status of all providers including component counts."""
    status = {}
    for name, provider in self.providers.items():
      if provider.detect_existing(project_dir):
        status[name] = provider.get_existing_components(project_dir)
      else:
        status[name] = {'config': False, 'commands': 0, 'prompts': 0, 'agents': False}
    return status

  def get_configured_providers(self, project_dir: Path) -> List[str]:
    """Get list of provider names that are already configured."""
    return [
      name for name, configured in self.detect_existing_providers(project_dir).items() if configured
    ]

  def format_provider_status(self, project_dir: Path) -> str:
    """Format provider status for display."""
    status = self.get_provider_status(project_dir)
    lines = []

    for name, components in status.items():
      if not any(
        [components['config'], components['commands'], components['prompts'], components['agents']]
      ):
        lines.append(f'{name}: not configured')
      else:
        parts = []
        if components['config']:
          parts.append('config✓')
        if components['commands']:
          parts.append(f"commands✓({components['commands']})")
        else:
          parts.append('commands✗')
        if components['prompts']:
          parts.append(f"prompts✓({components['prompts']})")
        else:
          parts.append('prompts✗')
        if components['agents']:
          parts.append('agents✓')
        elif name == 'claude':  # Only Claude uses agents by default
          parts.append('agents✗')

        lines.append(f"{name}: {' '.join(parts)}")

    return '\n'.join(lines)
