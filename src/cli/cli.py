"""Main CLI application for aiproj."""

import typer

from .commands.add import add
from .commands.clean import clean
from .commands.init import init
from .commands.list_providers import list_providers

app = typer.Typer(
  name='aiproj', help='Multi-AI project configuration manager', no_args_is_help=True
)

# Register commands
app.command()(init)
app.command()(add)
app.command('list')(list_providers)
app.command()(clean)

if __name__ == '__main__':
  app()
