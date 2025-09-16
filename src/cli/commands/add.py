"""Add AI provider configurations to existing project."""

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Prompt

from ...core.detector import ProjectDetector
from ...core.generator import ConfigGenerator

console = Console()


def add(
  provider: str = typer.Argument(None, help='Provider to add (claude, gemini, codex)'),
  claude: bool = typer.Option(False, '--claude', help='Add Claude Code'),
  gemini: bool = typer.Option(False, '--gemini', help='Add Gemini CLI'),
  codex: bool = typer.Option(False, '--codex', help='Add OpenAI Codex'),
  force: bool = typer.Option(False, '--force', help='Overwrite existing configs'),
  editor: bool = typer.Option(True, '--editor/--no-editor', help='Open config files in editor'),
  config: bool = typer.Option(False, '--config', help='Add only main config files'),
  commands: bool = typer.Option(False, '--commands', help='Add only command templates'),
  prompts: bool = typer.Option(False, '--prompts', help='Add only prompt templates'),
  agents: bool = typer.Option(False, '--agents', help='Add only agents configuration'),
  all_components: bool = typer.Option(False, '--all', help='Add all components'),
  migrate: bool = typer.Option(
    True, '--migrate/--no-migrate', help='Migrate content from existing providers'
  ),
):
  """Add AI provider configurations to existing project with content migration."""
  project_dir = Path.cwd()
  detector = ProjectDetector()
  generator = ConfigGenerator()

  # Show current status
  console.print('[bold cyan]Current configuration status:[/bold cyan]')
  console.print(detector.format_provider_status(project_dir))
  console.print()

  # Determine target provider
  if provider:
    target_provider = provider
  elif claude:
    target_provider = 'claude'
  elif gemini:
    target_provider = 'gemini'
  elif codex:
    target_provider = 'codex'
  else:
    # Prompt for provider
    existing = detector.detect_existing_providers(project_dir)
    available = [name for name, configured in existing.items() if not configured]

    if not available:
      console.print('[yellow]All providers are already configured.[/yellow]')
      return

    target_provider = Prompt.ask(
      'Which provider would you like to add?', choices=available, default=available[0]
    )

  # Check if target provider exists
  provider_obj = detector.get_provider(target_provider)
  if not provider_obj:
    console.print(f'[red]Unknown provider: {target_provider}[/red]')
    console.print(
      f"[yellow]Available providers: {', '.join(detector.get_all_providers().keys())}[/yellow]"
    )
    raise typer.Exit(1)

  # Check if target provider already exists
  if provider_obj.detect_existing(project_dir):
    console.print(f'[yellow]{target_provider} is already configured.[/yellow]')

    # Show what components exist and what's missing
    status = detector.get_provider(target_provider).get_existing_components(project_dir)
    missing_components = []
    if not status['config']:
      missing_components.append('config')
    if status['commands'] == 0:
      missing_components.append('commands')
    if status['prompts'] == 0:
      missing_components.append('prompts')
    if target_provider == 'claude' and not status['agents']:
      missing_components.append('agents')

    if missing_components:
      console.print(f"[cyan]Missing components: {', '.join(missing_components)}[/cyan]")
    else:
      console.print('[green]All components are configured.[/green]')
      if not force:
        return

  # Determine which components to add
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

  # Default to missing components if none specified
  if not components:
    if detector.get_provider(target_provider).detect_existing(project_dir):
      status = detector.get_provider(target_provider).get_existing_components(project_dir)
      components = []
      if not status['config']:
        components.append('config')
      if status['commands'] == 0:
        components.append('commands')
    else:
      components = ['config', 'commands']

  # Find source providers for migration
  migrate_from = []
  if migrate:
    configured = detector.get_configured_providers(project_dir)
    migrate_from = [p for p in configured if p != target_provider]

  console.print(
    f"\n[bold green]Adding {target_provider} with components: {', '.join(components)}[/bold green]"
  )
  if migrate_from:
    console.print(f"[cyan]Migrating content from: {', '.join(migrate_from)}[/cyan]")

  try:
    # Generate configuration files
    files = generator.generate_provider_config(
      project_dir=project_dir,
      provider_name=target_provider,
      components=components,
      migrate_from=migrate_from if migrate else None,
    )

    # Write files to disk
    written_files = generator.write_config_files(project_dir=project_dir, files=files, force=force)

    if written_files:
      console.print(f'[green]Created {len(written_files)} files:[/green]')
      for file_path in written_files:
        console.print(f'  • {file_path}')

      # Open in editor if requested
      if editor:
        generator.open_in_editor(project_dir, target_provider, components)
    else:
      console.print('[yellow]No new files created (use --force to overwrite)[/yellow]')

  except Exception as e:
    console.print(f'[red]Error adding {target_provider}: {e}[/red]')
    raise typer.Exit(1)

  # Show final status
  console.print('\n[bold cyan]Updated configuration status:[/bold cyan]')
  console.print(detector.format_provider_status(project_dir))
