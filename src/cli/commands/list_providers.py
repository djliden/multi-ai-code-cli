"""List AI provider configurations and status."""

from pathlib import Path

from rich.console import Console
from rich.table import Table

from ...core.detector import ProjectDetector

console = Console()


def list_providers():
  """List configured AI providers and their status."""
  project_dir = Path.cwd()
  detector = ProjectDetector()

  # Get detailed status for all providers
  status = detector.get_provider_status(project_dir)

  # Create table
  table = Table(title='AI Provider Configuration Status')
  table.add_column('Provider', style='bold')
  table.add_column('Config', justify='center')
  table.add_column('Commands', justify='center')
  table.add_column('Prompts', justify='center')
  table.add_column('Agents', justify='center')

  for name, components in status.items():
    # Format status indicators
    config_status = '✓' if components['config'] else '✗'
    commands_status = f"✓ ({components['commands']})" if components['commands'] > 0 else '✗'
    prompts_status = f"✓ ({components['prompts']})" if components['prompts'] > 0 else '✗'

    # Only show agents for Claude (others don't use it)
    if name == 'claude':
      agents_status = '✓' if components['agents'] else '✗'
    else:
      agents_status = '-'

    # Color the provider name based on configuration status
    provider_color = (
      'green'
      if any(
        [
          components['config'],
          components['commands'] > 0,
          components['prompts'] > 0,
          components['agents'],
        ]
      )
      else 'dim'
    )

    table.add_row(
      f'[{provider_color}]{name}[/{provider_color}]',
      config_status,
      commands_status,
      prompts_status,
      agents_status,
    )

  console.print(table)

  # Show summary
  configured_providers = [
    name
    for name, components in status.items()
    if any(
      [components['config'], components['commands'], components['prompts'], components['agents']]
    )
  ]

  if configured_providers:
    console.print(f"\n[green]Configured providers: {', '.join(configured_providers)}[/green]")
  else:
    console.print(
      "\n[yellow]No AI providers configured yet. Run 'aiproj init' to get started.[/yellow]"
    )
