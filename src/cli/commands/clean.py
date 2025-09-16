"""Clean (remove) AI provider configurations."""

import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt

from ...core.detector import ProjectDetector

console = Console()


def clean(
  provider: str = typer.Argument(None, help='Provider to remove (claude, gemini, codex)'),
  config: bool = typer.Option(False, '--config', help='Remove only main config files'),
  commands: bool = typer.Option(False, '--commands', help='Remove only command templates'),
  prompts: bool = typer.Option(False, '--prompts', help='Remove only prompt templates'),
  agents: bool = typer.Option(False, '--agents', help='Remove only agents configuration'),
  all_components: bool = typer.Option(False, '--all', help='Remove all components'),
  force: bool = typer.Option(False, '--force', help='Skip confirmation prompts'),
):
  """Remove AI provider configurations."""
  project_dir = Path.cwd()
  detector = ProjectDetector()

  # Show current status
  console.print('[bold cyan]Current configuration status:[/bold cyan]')
  console.print(detector.format_provider_status(project_dir))
  console.print()

  # Determine target provider
  if provider:
    target_provider = provider
  else:
    # Prompt for provider
    configured = detector.get_configured_providers(project_dir)

    if not configured:
      console.print('[yellow]No providers are configured.[/yellow]')
      return

    target_provider = Prompt.ask(
      'Which provider would you like to remove?',
      choices=configured + ['all'],
      default=configured[0] if len(configured) == 1 else 'all',
    )

  # Handle 'all' providers
  if target_provider == 'all':
    if not force and not Confirm.ask('[red]Remove all AI provider configurations?[/red]'):
      return

    for provider_name in detector.get_configured_providers(project_dir):
      _remove_provider(project_dir, provider_name, ['config', 'commands', 'prompts', 'agents'])

    console.print('[green]All providers removed.[/green]')
    return

  # Check if target provider exists
  provider_obj = detector.get_provider(target_provider)
  if not provider_obj or not provider_obj.detect_existing(project_dir):
    console.print(f'[yellow]{target_provider} is not configured.[/yellow]')
    return

  # Determine which components to remove
  components = []
  if config:
    components.append('config')
  if commands:
    components.append('commands')
  if prompts:
    components.append('prompts')
  if agents:
    components.append('agents')
  if all_components:
    components = ['config', 'commands', 'prompts', 'agents']

  # Default to all components if none specified
  if not components:
    components = ['config', 'commands', 'prompts', 'agents']

  # Confirm removal
  component_str = ', '.join(components) if len(components) < 4 else 'all components'
  if not force and not Confirm.ask(f'Remove {component_str} for {target_provider}?'):
    return

  # Remove components
  removed_items = _remove_provider(project_dir, target_provider, components)

  if removed_items:
    console.print(f'[green]Removed {len(removed_items)} items:[/green]')
    for item in removed_items:
      console.print(f'  • {item}')
  else:
    console.print('[yellow]No items were removed.[/yellow]')

  # Show final status
  console.print('\n[bold cyan]Updated configuration status:[/bold cyan]')
  console.print(detector.format_provider_status(project_dir))


def _remove_provider(project_dir: Path, provider_name: str, components: list) -> list:
  """Remove specified components for a provider."""
  removed_items = []

  if provider_name == 'claude':
    if 'config' in components:
      config_file = project_dir / 'CLAUDE.md'
      if config_file.exists():
        config_file.unlink()
        removed_items.append('CLAUDE.md')

    if 'commands' in components:
      commands_dir = project_dir / '.claude' / 'commands'
      if commands_dir.exists():
        shutil.rmtree(commands_dir)
        removed_items.append('.claude/commands/')

    # For Claude Code, prompts are stored as commands in .claude/commands/
    # No separate prompts directory to clean

    if 'agents' in components:
      agents_file = project_dir / 'agents.md'
      if agents_file.exists():
        agents_file.unlink()
        removed_items.append('agents.md')

    # Clean up empty .claude directory
    claude_dir = project_dir / '.claude'
    if claude_dir.exists() and not any(claude_dir.iterdir()):
      claude_dir.rmdir()
      removed_items.append('.claude/')

  elif provider_name in ['gemini', 'codex']:
    if 'config' in components:
      config_file = project_dir / f'.{provider_name}'
      if config_file.exists():
        if config_file.is_file():
          config_file.unlink()
        else:
          shutil.rmtree(config_file)
        removed_items.append(f'.{provider_name}')

    provider_dir = project_dir / f'.{provider_name}'
    if provider_dir.exists() and provider_dir.is_dir():
      if 'commands' in components:
        commands_dir = provider_dir / 'commands'
        if commands_dir.exists():
          shutil.rmtree(commands_dir)
          removed_items.append(f'.{provider_name}/commands/')

      if 'prompts' in components:
        prompts_dir = provider_dir / 'prompts'
        if prompts_dir.exists():
          shutil.rmtree(prompts_dir)
          removed_items.append(f'.{provider_name}/prompts/')

      # Clean up empty provider directory
      if not any(provider_dir.iterdir()):
        provider_dir.rmdir()

  return removed_items
