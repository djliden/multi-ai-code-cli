# Claude CLI App Template

This is a template for building Typer CLI applications with the help of Claude.

> **Note for Claude:** For template development tasks (modifying this template itself), refer to `claude_dev.md` instead of this file.

## Tech Stack

- Python with `uv` for package management
- Typer for the CLI framework
- Ruff for linting and formatting

## Development Workflow

### Package Management
- Use `uv add/remove` for Python dependencies.
- Edit `pyproject.toml` to manage your dependencies.

### Development Commands
- `./scripts/setup.sh` - Interactive environment setup and dependency installation
- `uv run python app.py --help` - Test the CLI application  
- `./scripts/test.sh` - Run the test suite
- `./app_status.sh` - Check project status and test coverage

## CLI Structure

This template follows the **one-file-per-command** approach recommended by Typer:

**Project Architecture:**
```
src/
├── cli/              # CLI interface layer only
│   ├── cli.py        # Main CLI app and command registration
│   └── commands/     # Individual command implementations
│       ├── __init__.py
│       ├── hello.py  # Thin CLI wrapper - calls src.core functions
│       └── goodbye.py
├── core/             # Core business logic and application services
├── models/           # Data models, schemas, domain objects
├── services/         # Database management, external APIs, AI agents
└── utils/            # Shared utility functions

tests/
├── test_hello.py     # CLI command tests
├── test_goodbye.py
├── test_core/        # Core business logic tests
└── test_models/      # Data model tests
```

**Key Principle:** CLI commands should be **thin interface layers** that parse arguments and call core business logic.

**Adding New Commands:**
1. Create `src/cli/commands/mycommand.py` with command function
2. Import and register in `src/cli/cli.py`
3. Create `tests/test_mycommand.py` with tests
4. Run `./app_status.sh` to verify test coverage

### Testing Your CLI
This template includes a robust testing setup with **one test file per command**:

**Running Tests:**
```bash
./scripts/test.sh              # Run all tests
uv run pytest tests/ -v        # Run tests with verbose output
uv run pytest tests/test_hello.py  # Run tests for specific command
```

**Writing Tests:**
Each command should have a corresponding test file. Use `CliRunner` to test CLI commands:

```python
from typer.testing import CliRunner
from src.cli.cli import app

runner = CliRunner()

def test_my_command():
    result = runner.invoke(app, ['my-command', '--arg', 'value'])
    assert result.exit_code == 0
    assert 'expected output' in result.output
```

**Test Coverage Verification:**
- `./app_status.sh` checks that every command file has a corresponding test file
- Status warns about missing test files without running slow tests
- Run `./scripts/test.sh` when you want to actually execute tests

### Claude Natural Language Commands
Claude understands natural language commands for common development tasks:

**Development:**
- "add a new command called X that does Y" - Creates new command file and registers it
- "add a parameter --flag to the existing command"
- "run the cli with arguments: hello world"

**Testing (Automated):**
- Claude will automatically create test files when adding new commands
- "write tests for the new command" - Adds comprehensive test coverage
- "test that invalid arguments show an error"
- "run the test suite and fix any failures"

**Examples:**
- "I want to add a 'list' command that shows files in a directory"
  → Creates `src/cli/commands/list.py` and `tests/test_list.py`
- "Add a --verbose flag to the list command"
- "Test the list command with different directory arguments"