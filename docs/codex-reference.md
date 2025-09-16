# OpenAI Codex CLI Reference

Quick reference for OpenAI Codex CLI capabilities and syntax.

## Core Concepts

**Codex CLI** - OpenAI's CLI tool for AI-assisted coding
**AGENTS.md** - Agent configuration file
**Custom Prompts** - Markdown files in `~/.codex/prompts/` (global Codex home)
**TUI Mode** - Interactive text interface

## Basic Usage

```bash
# Interactive mode (TUI)
codex

# Interactive with initial prompt
codex "fix lint errors"

# Non-interactive execution
codex exec "explain utils.ts"

# With model selection
codex -m gpt-4 "refactor this code"

# Request approval before changes
codex --ask-for-approval "modify database schema"
```

## File Operations

```bash
# Change working directory
codex --cd /path/to/project

# Include image input
codex -i screenshot.png "explain this UI"
```

## Custom Prompts

Create `.md` files in prompt directories:

**Global prompts:** `~/.codex/prompts/`
**Project templates:** `.codex/prompts/` *(copy or symlink into the global folder to enable slash commands)*

**Example: `~/.codex/prompts/python-debug.md`**
```markdown
Debug this Python code. Check for:
- Logic errors
- Performance issues
- Missing error handling
- Type safety problems
```

**Usage:**
1. Run `codex` (interactive mode)
2. Type `/` to see slash commands
3. Select your custom prompt from the list
4. Custom prompt content is submitted automatically

## Configuration

**AGENTS.md** - Project context:
```markdown
# Project Instructions
Python FastAPI project
Use type hints and async/await
Test with pytest
```

## Special Features

**File Search:** Use `@` trigger in TUI to search files
**Shell Completions:** Available for bash/zsh/fish
**Approval Mode:** `--ask-for-approval` for safety

## Common Patterns

**Setup:**
1. Create AGENTS.md for project context
2. Add custom prompts to `~/.codex/prompts/` (copy from `.codex/prompts/` if you track them in the repo)
3. Use interactive mode for exploration

**Workflows:**
- `codex exec` for automated tasks
- Custom prompts for repeated workflows
- File search with `@` for quick navigation
