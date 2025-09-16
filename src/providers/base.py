"""Base provider interface for AI coding tools."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Command:
  """Represents a custom command/prompt for an AI provider."""

  name: str
  description: str
  content: str
  metadata: Dict[str, Any] = None

  def __post_init__(self):
    if self.metadata is None:
      self.metadata = {}


@dataclass
class ProviderConfig:
  """Configuration and content detected from an existing provider setup."""

  main_config: Optional[str] = None
  commands: List[Command] = None
  prompts: List[Command] = None
  agents: Optional[str] = None
  additional_files: Dict[str, str] = None

  def __post_init__(self):
    if self.commands is None:
      self.commands = []
    if self.prompts is None:
      self.prompts = []
    if self.additional_files is None:
      self.additional_files = {}


class Provider(ABC):
  """Abstract interface for AI provider setup and content migration."""

  @property
  @abstractmethod
  def name(self) -> str:
    """Provider name (e.g., 'claude', 'gemini', 'codex')."""
    pass

  @property
  @abstractmethod
  def config_files(self) -> List[str]:
    """Main config files (e.g., ['CLAUDE.md'])."""
    pass

  @property
  @abstractmethod
  def directories(self) -> List[str]:
    """Required directories (e.g., ['.claude/commands', '.claude/prompts'])."""
    pass

  @abstractmethod
  def detect_existing(self, project_dir: Path) -> bool:
    """Check if provider is already configured."""
    pass

  @abstractmethod
  def load_existing_config(self, project_dir: Path) -> ProviderConfig:
    """Load existing configuration and content from project directory."""
    pass

  @abstractmethod
  def generate_config(
    self,
    project_dir: Path,
    components: List[str] = None,
    base_config: Optional[ProviderConfig] = None,
  ) -> Dict[str, str]:
    """Generate config files for specified components. Returns {filepath: content}."""
    pass

  @abstractmethod
  def get_existing_components(self, project_dir: Path) -> Dict[str, Any]:
    """Get status of existing components (config, commands count, prompts count, agents)."""
    pass

  @abstractmethod
  def get_editor_files(self, project_dir: Path, components: List[str] = None) -> List[str]:
    """Files to open in editor after generation for specified components."""
    pass

  def migrate_content_from(self, source_config: ProviderConfig) -> ProviderConfig:
    """Migrate content from another provider's configuration.

    Default implementation copies commands and prompts directly.
    """
    return ProviderConfig(
      commands=source_config.commands.copy(),
      prompts=source_config.prompts.copy(),
      agents=source_config.agents,
      additional_files=source_config.additional_files.copy(),
    )
