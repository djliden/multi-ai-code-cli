# Multi-AI Project Configuration Tool

A CLI tool for managing AI provider configurations across different AI coding assistants (Claude Code, Gemini CLI, OpenAI Codex) in your projects.

## Installation

### Install from GitHub
```bash
# Install directly from GitHub using pip
pip install git+https://github.com/your-username/multi-ai-code-template.git

# Or using uv (recommended)
uv tool install git+https://github.com/your-username/multi-ai-code-template.git
```

### Local Development Installation
```bash
git clone https://github.com/your-username/multi-ai-code-template.git
cd multi-ai-code-template
uv sync
uv run python app.py --help
```

## Usage

The `aiproj` tool helps you manage AI provider configurations across different AI coding assistants:

### Initialize AI Provider Configurations
```bash
# Initialize Claude Code configuration
aiproj init --claude

# Initialize multiple providers at once
aiproj init --claude --gemini --codex

# Initialize with specific components only
aiproj init --claude --config --commands
```

### Add New Providers to Existing Project
```bash
# Add a new provider with content migration from existing providers
aiproj add gemini --migrate

# Add without migration (clean slate)
aiproj add codex --no-migrate

# Add specific components only
aiproj add claude --commands --prompts
```

### List Provider Status
```bash
aiproj list
```

### Clean Up Provider Configurations
```bash
# Remove specific provider
aiproj clean claude

# Remove all providers
aiproj clean all

# Remove specific components only
aiproj clean claude --commands --force
```

## What It Does

This tool manages configuration files for different AI coding assistants in your projects:

### Supported AI Providers

- **Claude Code**: Creates `CLAUDE.md`, `.claude/commands/`, `agents.md`
- **Gemini CLI**: Creates `.gemini/config`, `.gemini/commands/`, `.gemini/prompts/`
- **OpenAI Codex**: Creates `.codex/config`, `.codex/commands/`, `.codex/prompts/`

> Note: The current implementation provides a unified interface for managing these AI providers. Future versions will align more closely with each provider's native configuration format.

### Key Features

- **🔄 Content Migration**: Automatically migrates existing commands and prompts between providers
- **🎯 Component Selection**: Choose which components to initialize (config, commands, prompts, agents)
- **📊 Status Overview**: See which providers are configured and what components exist
- **🧹 Smart Cleanup**: Remove specific providers or components safely
- **🚀 Interactive Setup**: Prompts guide you through configuration choices

### Example Workflow

```bash
# Start with Claude Code in your project
aiproj init --claude

# Later, add Gemini and migrate your existing Claude commands
aiproj add gemini --migrate

# Check status of all providers
aiproj list

# Clean up if needed
aiproj clean codex
```

## Development

Built with:
- 🔧 **Typer**: Modern CLI framework
- 🎨 **Rich**: Beautiful terminal output
- ⚡ **uv**: Fast Python package management
- 🧪 **pytest**: Comprehensive test suite
- 🛠️ **ruff**: Code formatting and linting
