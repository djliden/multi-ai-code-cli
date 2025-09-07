# Claude Code CLI Reference

Quick reference for Claude Code CLI capabilities and syntax.

## Core Concepts

**Claude Code** - Official Anthropic CLI for Claude AI assistance with coding tasks
**CLAUDE.md** - Project instructions file (analogous to README for Claude)
**Slash Commands** - Custom commands defined in `.claude/commands/`
**Subagents** - Specialized AI agents for specific task types
**Hooks** - Shell commands that execute on events (tool calls, etc.)

## Basic Usage

```bash
# Interactive session
claude

# Direct command
claude "analyze this function"

# With file context
claude --files src/main.py "optimize this code"
```

## Configuration Files

**CLAUDE.md** - Project instructions and context
```markdown
# Project Instructions
Tech stack: Python, FastAPI
Always use type hints
Run tests with: pytest
```

**settings.json** - CLI configuration
```json
{
  "defaultModel": "claude-3-5-sonnet-20241022",
  "maxTokens": 4096,
  "temperature": 0
}
```

## Custom Slash Commands

Create commands in `.claude/commands/command-name.md`:

```markdown
---
description: "Brief command description"
---

# Command Implementation
Your prompt instructions here.
```

Usage: `/command-name arguments`

## Memory Management

**Project Memory** - Automatic context from CLAUDE.md
**Session Memory** - Conversation history within session
**File Memory** - Automatic context from recently edited files

## Tool Capabilities

- File read/write operations
- Git integration
- Shell command execution  
- Web search and fetch
- Code analysis and refactoring
- Test generation and execution

## Common Patterns

**Project Setup:**
1. Create CLAUDE.md with project context
2. Define custom commands in .claude/commands/
3. Configure settings.json for preferences

**Development Workflow:**
1. Use natural language for complex tasks
2. Leverage slash commands for repeated patterns
3. Let Claude handle file operations and testing