"""Shared test configuration."""

import sys
from pathlib import Path

# test_decorators.py imports `from decorators import input_error` (bare import),
# so we add handlers/ to sys.path.
_handlers_dir = str(Path(__file__).resolve().parent.parent / "handlers")
if _handlers_dir not in sys.path:
    sys.path.insert(0, _handlers_dir)
