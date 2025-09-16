"""Test configuration and utilities."""

import os
import tempfile
from contextlib import contextmanager
from pathlib import Path

from typer.testing import CliRunner


@contextmanager
def temp_project_dir():
  """Context manager for temporary project directory with proper cwd handling."""
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    original_cwd = os.getcwd()
    try:
      os.chdir(temp_path)
      yield temp_path
    finally:
      os.chdir(original_cwd)


def run_cli_command(command_args):
  """Run a CLI command and return the result."""
  runner = CliRunner()
  from src.cli.cli import app

  return runner.invoke(app, command_args)
