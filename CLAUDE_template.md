# Claude CLI App Template

This is a template for building Typer CLI applications with the help of Claude.

## Tech Stack

- Python with `uv` for package management
- Typer for the CLI framework
- Ruff for linting and formatting

## Development Workflow

### Package Management
- Use `uv add/remove` for Python dependencies.
- Edit `pyproject.toml` to manage your dependencies.

### Development Commands
- `scripts/setup.sh` - Interactive environment setup and dependency installation.
- `uv run python src/claude_cli_app/cli.py` - Run the CLI application.

### Claude Natural Language Commands
Claude understands natural language commands for common development tasks:

- "add a new command" - Creates a new Typer command.
- "add a new parameter to the existing command"
- "run the cli with the following arguments: ..."