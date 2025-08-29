# Claude CLI App Template (Typer)

A minimal template for building CLI apps with Typer, inspired by the Databricks one-command workflow. It provides an interactive flow to set up your environment and generate product and design docs.

## Quickstart

- Create a virtual env and install:
  ```bash
  ./scripts/setup.sh
  source .venv/bin/activate
  ```
- Run checks:
  ```bash
  cla check
  ```
- Kick off the guided flow:
  ```bash
  cla spec
  ```

## Commands
- `cla init` — Print/setup guidance (calls `./scripts/setup.sh`)
- `cla check` — Basic environment checks
- `cla reqs` — Interactive product requirements → `docs/product.md`
- `cla design` — Interactive technical design → `docs/design.md`
- `cla spec` — Opinionated end-to-end flow (setup hint → reqs → design)

## Structure
- `src/claude_cli_app/cli.py` — Typer app entrypoint
- `scripts/` — Setup scripts, dependency checks
- `docs/` — Generated documentation (requirements/design)
- `CLAUDE.md` — Development guide for this template

## Notes
- This repo adapts concepts from `databricks-solutions/claude-databricks-app-template` to a pure CLI context.
- You can extend `cla dba` to also scaffold project skeletons, plugins, and CI later.
