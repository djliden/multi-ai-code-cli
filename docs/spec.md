# Spec (CLI) Workflow

This document describes the CLI-first adaptation of the one-command development flow.

## Goal
Provide a single command that guides you from idea → requirements → technical design for CLI projects.

## Command
```bash
cla spec
```

## Steps
1. Confirm environment setup (points to `./scripts/setup.sh`).
2. Gather product requirements → writes `docs/product.md`.
3. Create technical design → writes `docs/design.md`.

## Artifacts
- `docs/product.md` — Product Requirements Document
- `docs/design.md` — Technical Design Document

## Notes
- Re-run `cla reqs` and `cla design` to iterate.
- The flow is intentionally minimal; extend it to scaffold CLI subcommands or plugins as needed.

