# Gemini CLI Reference

Quick reference for Google Gemini CLI capabilities and syntax.

## Core Concepts

**Gemini CLI** - Google's official CLI for Gemini AI models
**GEMINI.md** - Project context file (analogous to CLAUDE.md)
**Custom Commands** - TOML-based slash commands  
**.geminiignore** - Files to exclude from context

## Basic Usage

```bash
# Interactive mode
gemini

# Direct prompt
gemini -p "explain this code"

# Include directories
gemini --include-directories src,tests

# Non-interactive mode
gemini -p "task" --no-input
```

## Authentication Options

```bash
# OAuth flow (recommended)
gemini auth login

# API key
export GOOGLE_API_KEY="your-key"

# Vertex AI (GCP projects)
gemini auth vertex-ai
```

## Configuration Files

**GEMINI.md** - Project instructions
```markdown
# Project Context
This is a Python CLI project using Typer and pytest.
```

**Custom Commands** - `.toml` files in project root:
```toml
[command.review]
description = "Code review assistant"
prompt = "Review this code for bugs and improvements"
```

## Model Selection

```bash
# Default (gemini-1.5-flash)
gemini -p "task"

# Specific model
gemini -m gemini-1.5-pro -p "complex task"
```

## Directory Inclusion

```bash
# Include specific directories
gemini --include-directories src,docs -p "analyze structure"

# Exclude with .geminiignore
# Similar to .gitignore syntax
*.pyc
__pycache__/
.env
```

## Common Patterns

**Project Setup:**
1. Create GEMINI.md for context
2. Set up .geminiignore for file filtering
3. Configure custom .toml commands for workflows

**Development Use:**
- Interactive mode for exploration
- `--include-directories` for focused analysis
- Custom commands for repeated tasks