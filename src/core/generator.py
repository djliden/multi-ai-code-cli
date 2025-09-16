"""Core generator logic for AI provider configurations."""

import os
from pathlib import Path
from typing import Dict, List

from ..providers.base import ProviderConfig
from .detector import ProjectDetector


class ConfigGenerator:
  """Generate AI provider configurations with content migration."""

  def __init__(self):
    self.detector = ProjectDetector()

  def generate_provider_config(
    self,
    project_dir: Path,
    provider_name: str,
    components: List[str] = None,
    migrate_from: List[str] = None,
  ) -> Dict[str, str]:
    """Generate configuration for a provider, optionally migrating content from others.

    Args:
        project_dir: Target project directory
        provider_name: Provider to generate config for
        components: List of components to generate (config, commands, prompts, agents)
        migrate_from: List of provider names to migrate content from

    Returns:
        Dict mapping file paths to content
    """
    provider = self.detector.get_provider(provider_name)
    if not provider:
      raise ValueError(f'Unknown provider: {provider_name}')

    # Load existing content from source providers
    base_config = None
    if migrate_from:
      base_config = self._merge_source_configs(project_dir, migrate_from)

    # Generate new configuration
    return provider.generate_config(project_dir, components, base_config)

  def write_config_files(
    self, project_dir: Path, files: Dict[str, str], force: bool = False
  ) -> List[str]:
    """Write configuration files to disk.

    Args:
        project_dir: Target directory
        files: Dict of filepath -> content
        force: Overwrite existing files

    Returns:
        List of files that were written
    """
    written_files = []

    for file_path, content in files.items():
      full_path = project_dir / file_path

      # Check if file exists and force is not set
      if full_path.exists() and not force:
        continue

      # Handle case where parent directory conflicts with existing file
      parent = full_path.parent
      if parent.exists() and parent.is_file():
        if force:
          parent.unlink()  # Remove conflicting file
        else:
          continue

      # Create directory if needed
      parent.mkdir(parents=True, exist_ok=True)

      # Write file
      full_path.write_text(content)
      written_files.append(file_path)

    return written_files

  def open_in_editor(
    self, project_dir: Path, provider_name: str, components: List[str] = None
  ) -> bool:
    """Open generated config files in editor.

    Args:
        project_dir: Project directory
        provider_name: Provider name
        components: Components that were generated

    Returns:
        True if editor was launched successfully
    """
    provider = self.detector.get_provider(provider_name)
    if not provider:
      return False

    files_to_open = provider.get_editor_files(project_dir, components)
    if not files_to_open:
      return False

    # Try to launch editor (simple implementation)
    editor = os.environ.get('EDITOR', 'code')  # Default to VS Code

    try:
      import subprocess

      for file_path in files_to_open:
        full_path = project_dir / file_path
        if full_path.exists():
          subprocess.run([editor, str(full_path)], check=False)
      return True
    except (subprocess.SubprocessError, FileNotFoundError):
      return False

  def _merge_source_configs(self, project_dir: Path, source_providers: List[str]) -> ProviderConfig:
    """Merge configuration from multiple source providers."""
    merged_config = ProviderConfig()

    for provider_name in source_providers:
      provider = self.detector.get_provider(provider_name)
      if provider and provider.detect_existing(project_dir):
        source_config = provider.load_existing_config(project_dir)

        # Merge main config (use first non-empty one)
        if source_config.main_config and not merged_config.main_config:
          merged_config.main_config = source_config.main_config

        # Merge commands (combine all)
        merged_config.commands.extend(source_config.commands)

        # Merge prompts (combine all)
        merged_config.prompts.extend(source_config.prompts)

        # Merge agents (use first non-empty one)
        if source_config.agents and not merged_config.agents:
          merged_config.agents = source_config.agents

        # Merge additional files
        merged_config.additional_files.update(source_config.additional_files)

    return merged_config
