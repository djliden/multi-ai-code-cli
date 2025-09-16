# Claude Code Configuration

## Multi-AI Project Configuration Tool

This is a CLI tool (`aiproj`) for managing AI provider configurations across different AI coding assistants:
- **Claude Code**: CLAUDE.md, .claude/commands/, agents.md
- **Gemini CLI**: .gemini/config, .gemini/commands/, .gemini/prompts/
- **OpenAI Codex**: .codex/config, .codex/commands/, .codex/prompts/

## Tech Stack
- **Language**: Python 3.12+
- **CLI Framework**: Typer with Rich for beautiful terminal output
- **Package Manager**: uv for fast dependency management
- **Testing**: pytest with comprehensive test coverage
- **Linting**: ruff for code formatting and linting

## Key Components
- `src/providers/`: Provider implementations (claude.py, gemini.py, codex.py)
- `src/cli/`: CLI command implementations
- `src/core/`: Core detection and generation logic
- `tests/`: Comprehensive test suite

## Testing
Run tests with: `uv run pytest`
Run specific tests: `uv run pytest tests/test_providers.py -v`
Run with coverage: `uv run pytest --cov=src`

## Linting
Format code: `uv run ruff format`
Check linting: `uv run ruff check`
Fix linting: `uv run ruff check --fix`

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
