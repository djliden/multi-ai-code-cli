# Gemini CLI Reference for aiproj

Essential configuration reference for setting up Gemini CLI within the `aiproj` multi-AI setup tool.

## Core Configuration Files

### 1. Context File: `GEMINI.md`
**Purpose**: Project context and instructions (equivalent to `CLAUDE.md` for Claude Code)
**Location**: Project root directory

**Example Structure:**
```markdown
# Project Context for Gemini CLI

## Project Overview
[Brief description of your project and its goals]

## Tech Stack
- Python 3.8+ with Typer CLI framework
- [Other relevant technologies]

## Development Workflow
- [Key development patterns]
- [Testing approach]
- [Code review process]

## Custom Commands Available
- `/docs` - Generate documentation
- `/test` - Create and run tests
- `/review` - Perform code review
- `/refactor` - Improve code structure

## Important Notes
[Any project-specific guidance for AI assistance]
```

### 2. Project Configuration: `.geminiignore`
**Purpose**: Define which files/directories to include/exclude from context
**Format**: Similar to `.gitignore`

**Example:**
```gitignore
# Build artifacts
/dist/
/build/
*.pyc
__pycache__/

# Dependencies
node_modules/
venv/

# Include important files
!README.md
!pyproject.toml
```

## Custom Slash Commands

### Directory Structure
```
.gemini/
└── commands/
    ├── docs.toml
    ├── test.toml
    ├── review.toml
    └── git/
        └── commit.toml    # Creates /git:commit command
```

### Command Format (TOML)
**Required fields:**
- `prompt` - The prompt template

**Optional fields:**
- `description` - Command description for help

### Example Commands

**Documentation Command** (`.gemini/commands/docs.toml`):
```toml
description = "Generate comprehensive documentation"
prompt = """
Generate documentation for this codebase focusing on:
- API documentation
- Usage examples  
- Implementation details

{{args}}
"""
```

**Code Review Command** (`.gemini/commands/review.toml`):
```toml
description = "Perform thorough code review"
prompt = """
Review the following code for:
- Code quality and best practices
- Security issues
- Performance concerns
- Documentation completeness

{{args}}
"""
```

**Testing Command** (`.gemini/commands/test.toml`):
```toml
description = "Generate comprehensive tests"
prompt = """
Generate tests for the specified code including:
- Unit tests
- Integration tests
- Edge cases
- Proper mocking

{{args}}
"""
```

**Refactoring Command** (`.gemini/commands/refactor.toml`):
```toml
description = "Refactor code for better maintainability" 
prompt = """
Refactor this code to improve:
- Code structure and readability
- Performance
- Maintainability
- Follow best practices

{{args}}
"""
```

## Argument Handling

**Direct injection with `{{args}}`:**
```toml
prompt = "Review this code: {{args}}"
```

**Default behavior (no `{{args}}`):**
- Arguments are appended to the end of the prompt

## Advanced Features

**Shell command execution:**
```toml
prompt = """
Generate a commit message for these changes:

```diff
!{git diff --staged}
```
"""
```

**File content injection:**
```toml
prompt = """
Review the following file:
@{src/main.py}

{{args}}
"""
```