"""Initialize AI provider configurations."""

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Prompt

from ...core.detector import ProjectDetector
from ...core.generator import ConfigGenerator

console = Console()


def init(
  claude: bool = typer.Option(False, '--claude', help='Initialize Claude Code'),
  gemini: bool = typer.Option(False, '--gemini', help='Initialize Gemini CLI'),
  codex: bool = typer.Option(False, '--codex', help='Initialize OpenAI Codex'),
  force: bool = typer.Option(False, '--force', help='Overwrite existing configs'),
  editor: bool = typer.Option(True, '--editor/--no-editor', help='Open config files in editor'),
  config: bool = typer.Option(False, '--config', help='Generate only main config files'),
  commands: bool = typer.Option(False, '--commands', help='Generate only command templates'),
  prompts: bool = typer.Option(False, '--prompts', help='Generate only prompt templates'),
  agents: bool = typer.Option(False, '--agents', help='Generate only agents configuration'),
  all_components: bool = typer.Option(False, '--all', help='Generate all components'),
):
  """Initialize AI provider configurations for a project."""
  project_dir = Path.cwd()
  detector = ProjectDetector()
  generator = ConfigGenerator()

  # Determine which providers to initialize
  selected_providers = []
  if claude:
    selected_providers.append('claude')
  if gemini:
    selected_providers.append('gemini')
  if codex:
    selected_providers.append('codex')

  # If no providers specified, detect and prompt
  if not selected_providers:
    existing = detector.detect_existing_providers(project_dir)

    if any(existing.values()):
      console.print('\n[bold cyan]Detected existing configurations:[/bold cyan]')
      console.print(detector.format_provider_status(project_dir))
      console.print()

      missing = [name for name, configured in existing.items() if not configured]
      if missing:
        response = Prompt.ask(
          f"Add missing providers? [{','.join(missing)}]",
          choices=missing + ['none', 'all'],
          default='none',
        )
        if response == 'all':
          selected_providers = missing
        elif response in missing:
          selected_providers = [response]
    else:
      console.print('[yellow]No AI provider configurations detected.[/yellow]')
      response = Prompt.ask(
        'Which providers would you like to initialize?',
        choices=['claude', 'gemini', 'codex', 'all'],
        default='claude',
      )
      if response == 'all':
        selected_providers = ['claude', 'gemini', 'codex']
      else:
        selected_providers = [response]

  if not selected_providers:
    console.print('[yellow]No providers selected. Exiting.[/yellow]')
    return

  # Determine which components to generate
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

  # Default to config and commands if no components specified
  if not components:
    components = ['config', 'commands']

  # Initialize each selected provider
  for provider_name in selected_providers:
    console.print(f'\n[bold green]Initializing {provider_name}...[/bold green]')

    # Validate provider exists
    if not detector.get_provider(provider_name):
      console.print(f'[red]Unknown provider: {provider_name}[/red]')
      continue

    try:
      # Generate configuration files
      files = generator.generate_provider_config(
        project_dir=project_dir, provider_name=provider_name, components=components
      )

      # Write files to disk
      written_files = generator.write_config_files(
        project_dir=project_dir, files=files, force=force
      )

      if written_files:
        console.print(f'[green]Created {len(written_files)} files:[/green]')
        for file_path in written_files:
          console.print(f'  • {file_path}')

        # Open in editor if requested
        if editor:
          generator.open_in_editor(project_dir, provider_name, components)
      else:
        console.print(
          f'[yellow]No new files created for {provider_name} (use --force to overwrite)[/yellow]'
        )

    except Exception as e:
      console.print(f'[red]Error initializing {provider_name}: {e}[/red]')

  # Show final status
  console.print('\n[bold cyan]Final configuration status:[/bold cyan]')
  console.print(detector.format_provider_status(project_dir))
