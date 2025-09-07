# Technical Architecture Design

## aiproj CLI - Multi-AI Command Template Manager

### System Overview

A CLI tool focused on setting up and managing **custom commands and prompts** for multiple AI coding providers (Claude Code, Gemini CLI, OpenAI Codex). Emphasizes minimal setup, smart detection, and non-railroad configuration.

### Core Philosophy

1. **Detection First**: Check existing configs before asking questions
2. **Minimal Setup**: Generate structure, open editor, let user fill details
3. **Non-Interactive Support**: Full CLI flag support for automation
4. **Command/Prompt Focus**: Manage provider-specific commands, not tools themselves

### CLI Interface Design

#### Command Structure
```bash
# Interactive mode (smart detection)
aiproj init                    # Detect existing + guided setup
aiproj add                     # Add providers to existing project

# Non-interactive mode  
aiproj init --claude --gemini --codex    # Generate all three
aiproj init --claude --force             # Force overwrite existing
aiproj add --gemini --editor             # Add Gemini + open editor

# Management commands
aiproj list                    # Show configured providers
aiproj clean [--provider]     # Remove provider configs
```

#### Provider Flags
- `--claude` - Set up Claude Code commands/prompts
- `--gemini` - Set up Gemini CLI commands/prompts  
- `--codex` - Set up OpenAI Codex commands/prompts
- `--force` - Overwrite existing configs
- `--editor` - Open config files in editor after generation
- `--no-editor` - Skip editor opening

### Project Structure Generated

#### Claude Code Setup
```
CLAUDE.md                 # Main Claude configuration
.claude/
├── commands/             # Custom slash commands
│   ├── docs.md          # /docs command for documentation
│   ├── test.md          # /test command for testing
│   ├── refactor.md      # /refactor command  
│   └── review.md        # /review command
└── prompts/             # Reusable prompt templates
    ├── code-review.md
    ├── documentation.md
    └── bug-fix.md
```

#### Gemini CLI Setup  
```
.gemini                   # Main Gemini configuration file
.gemini/
├── commands/             # Gemini-specific commands
│   ├── docs.md
│   ├── test.md
│   └── refactor.md
└── prompts/
    ├── code-review.md
    └── optimization.md
```

#### OpenAI Codex Setup
```
.codex                    # Main Codex configuration
.codex/
├── commands/             # Codex-specific commands
└── prompts/              # Codex prompt templates
```

### Core Components Architecture

#### 1. CLI Interface (`src/cli/`)
```
src/cli/
├── cli.py              # Main aiproj CLI app
└── commands/
    ├── init.py         # aiproj init [--providers]
    ├── add.py          # aiproj add [--providers]  
    ├── list.py         # aiproj list
    └── clean.py        # aiproj clean
```

#### 2. Provider Detection & Management (`src/core/`)
```
src/core/
├── detector.py         # Detect existing provider configs
├── generator.py        # Generate provider directory structures
├── editor.py          # Launch editor for config files
└── template_loader.py  # Load command/prompt templates
```

#### 3. Provider Definitions (`src/providers/`)
```
src/providers/
├── base.py            # Abstract provider interface
├── claude.py          # Claude Code provider setup
├── gemini.py          # Gemini CLI provider setup  
└── codex.py           # OpenAI Codex provider setup
```

#### 4. Templates (`templates/`)
```
templates/
├── claude/
│   ├── CLAUDE.md.template    # Main config template
│   ├── commands/             # Starter command templates
│   │   ├── docs.md
│   │   ├── test.md
│   │   └── refactor.md
│   └── prompts/              # Starter prompt templates
│       └── code-review.md
├── gemini/
│   ├── .gemini.template      # Main config template  
│   ├── commands/
│   └── prompts/
└── codex/
    ├── .codex.template
    ├── commands/
    └── prompts/
```

### Command Flow Design

#### `aiproj init` Flow
```
1. Detect existing configs (CLAUDE.md, .gemini/, .codex/)
2. If found: "Found Claude setup. Add others? [gemini,codex]"  
3. If none found: "Which providers? [claude,gemini,codex]"
4. Generate directory structure for selected providers
5. Populate with starter command/prompt templates
6. Open main config files in editor (unless --no-editor)
7. Summary: "Generated configs for: claude, gemini"
```

#### `aiproj add` Flow
```
1. Detect existing project structure
2. Show already configured providers
3. Prompt for additional providers to add
4. Generate new provider configurations  
5. Open new config files in editor
6. Update project metadata
```

### Provider Interface Design

```python
# src/providers/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict

class Provider(ABC):
    """Abstract interface for AI provider setup."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'claude', 'gemini')."""
    
    @property
    @abstractmethod
    def config_files(self) -> List[str]:
        """Main config files (e.g., ['CLAUDE.md'])."""
    
    @property  
    @abstractmethod
    def directories(self) -> List[str]:
        """Required directories (e.g., ['.claude/commands'])."""
    
    @abstractmethod
    def detect_existing(self, project_dir: Path) -> bool:
        """Check if provider is already configured."""
    
    @abstractmethod
    def generate_config(self, project_dir: Path) -> Dict[str, str]:
        """Generate config files. Returns {filepath: content}."""
    
    @abstractmethod
    def get_editor_files(self) -> List[str]:
        """Files to open in editor after generation."""
```

### Configuration Management

#### Global Config (`~/.aiproj/config.toml`)
```toml
[defaults]
providers = ["claude"]
editor = "code"  # or "vim", "emacs", etc.
auto_open_editor = true

[providers.claude]
default_model = "claude-3-5-sonnet"

[providers.gemini]  
default_model = "gemini-pro"
```

#### Project Metadata (`.aiproj/meta.json`)
```json
{
  "providers": ["claude", "gemini"],
  "created_at": "2024-01-01T00:00:00Z",
  "last_updated": "2024-01-01T00:00:00Z"
}
```

### Smart Detection Logic

```python
def detect_providers(project_dir: Path) -> Dict[str, bool]:
    """Detect which providers are already configured."""
    return {
        "claude": (project_dir / "CLAUDE.md").exists() or 
                 (project_dir / ".claude").exists(),
        "gemini": (project_dir / ".gemini").exists(),
        "codex": (project_dir / ".codex").exists()
    }
```

### Editor Integration

- Automatically open main config files after generation
- Support multiple editors: VS Code, Vim, Emacs, etc.
- Configurable via global config or `--editor` flag
- Skip with `--no-editor` flag

### Error Handling

- **File Conflicts**: Detect existing files, require `--force` to overwrite
- **Missing Templates**: Graceful fallback to basic templates
- **Editor Errors**: Continue execution if editor fails to open
- **Permission Errors**: Clear messages for file/directory creation issues

This architecture focuses on the core need: **easy setup of AI provider command structures** with minimal user friction.
