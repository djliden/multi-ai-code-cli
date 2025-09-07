# OpenAI Codex Reference

Essential reference for OpenAI Codex integration in the aiproj CLI template.

## Configuration Files

**Instructions File:** `AGENTS.md` (equivalent to Claude's `CLAUDE.md`)

**Location Priority:**
1. `~/.codex/AGENTS.md` - Global personal guidance
2. `AGENTS.md` at repo root - Project-specific notes  
3. `AGENTS.md` in current directory - Sub-folder specifics

## Custom Slash Commands

**Location:** `~/.codex/prompts/`
- Create `.md` files in this directory
- Each file becomes a custom slash command
- File name = command name (e.g., `test.md` → `/test`)

**Usage:**
1. Launch `codex` (TUI mode)
2. Type `/` to see available commands
3. Select custom command from popup