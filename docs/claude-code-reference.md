# Claude Code Reference

Technical reference for Claude Code configuration system and custom commands.

## Project Structure

### Core Configuration Files
```
CLAUDE.md                    # Project memory/instructions (version controlled)
.claude/
├── settings.json           # Shared project settings (version controlled)
├── settings.local.json     # Personal settings (not version controlled)
├── commands/               # Custom slash commands directory
└── agents/                 # Custom subagents directory (optional)
```

### Configuration Hierarchy (highest to lowest priority)
1. Enterprise Managed Policies
2. Command Line Arguments
3. Local Project Settings (`.claude/settings.local.json`)
4. Shared Project Settings (`.claude/settings.json`)
5. User Settings (`~/.claude/settings.json`)

## CLAUDE.md File Format

Project memory file that provides context and instructions to Claude Code.

### Basic Structure
```markdown
# Project Title

Project description and context.

## Technical Details
- Framework information
- Key dependencies
- Build/test commands

## Development Guidelines
- Coding standards
- Project conventions
- Workflow instructions

## File Imports
@path/to/other/file.md
@docs/standards.md
```

### Import Syntax
- Use `@path/to/file` to import external files
- Supports recursive imports (max 5 levels deep)
- Relative paths from project root

## Settings Configuration

### JSON Structure
```json
{
  "permissions": {
    "allow": ["tool_pattern", "specific_command"],
    "deny": ["sensitive_pattern", "dangerous_command"]
  },
  "env": {
    "VARIABLE_NAME": "value"
  }
}
```

### Permission Patterns
- `Bash(command)` - Specific bash command
- `Bash(pattern*)` - Bash command patterns
- `Read(path)` - File read permissions
- `Write(path)` - File write permissions
- `Edit(path)` - File edit permissions

### Example Settings
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Read(src/**)",
      "Write(src/**)",
      "Edit(src/**)"
    ],
    "deny": [
      "Read(.env*)",
      "Read(*.key)",
      "Bash(rm *)"
    ]
  },
  "env": {
    "NODE_ENV": "development"
  }
}
```

## Custom Slash Commands

### File Organization
- Location: `.claude/commands/`
- Filename becomes command name (without `.md` extension)
- Supports subdirectories for namespacing

### Command File Format
```markdown
---
description: "Brief command description"
argument-hint: "<required> [optional]"
allowed-tools: ["Tool1", "Tool2"]
model: "specific-model-name"
---

Command instructions and behavior.

Use $ARGUMENTS for all arguments.
Use $1, $2, etc. for specific positional arguments.
```

### Frontmatter Options
- `description` - Brief explanation of command purpose
- `argument-hint` - Usage guidance for arguments
- `allowed-tools` - Restrict tools available to command
- `model` - Specify AI model for command

### Argument Handling
- `$ARGUMENTS` - All provided arguments as single string
- `$1`, `$2`, `$3`, etc. - Individual positional arguments
- Arguments are space-separated when command is invoked

### Advanced Features
```markdown
# File references
@src/example.py

# Bash command execution
!git status

# Multi-line instructions with specific steps
1. First do this
2. Then do that
3. Finally check results
```

## Global User Configuration

### User Settings Location
- macOS/Linux: `~/.claude/settings.json`
- User commands: `~/.claude/commands/`
- User memory: `~/.claude/CLAUDE.md`

### Enterprise Policies
- macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
- Linux/WSL: `/etc/claude-code/managed-settings.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

## Configuration Management

### CLI Commands
```bash
claude config list                    # Show all settings
claude config get <key>              # Get specific setting
claude config set <key> <value>      # Set configuration value
claude config add <key> <value>      # Add to array setting
claude config remove <key> <value>   # Remove from array setting
```

### Memory Management
```bash
claude /memory                        # Edit project memory
claude /init                         # Bootstrap project memory
claude #"quick memory addition"      # Add quick memory note
```

## File Naming Conventions

### Command Files
- Use descriptive names: `generate-docs.md`, `run-tests.md`
- Avoid spaces in filenames
- Use hyphens or underscores for separation
- Command name matches filename (without extension)

### Configuration Files
- `settings.json` - Shared project settings
- `settings.local.json` - Personal/local settings
- `CLAUDE.md` - Project memory (uppercase filename)

## Security Considerations

### Permission Best Practices
- Use specific patterns rather than wildcards when possible
- Explicitly deny access to sensitive files
- Use `.claude/settings.local.json` for personal configurations
- Regularly audit permission settings

### Sensitive Data
- Never commit API keys in settings files
- Use environment variables for secrets
- Add sensitive patterns to `permissions.deny`
- Keep personal settings in local-only files