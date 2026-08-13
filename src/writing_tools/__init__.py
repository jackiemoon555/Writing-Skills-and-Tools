"""Writing-Skills-and-Tools: composable utilities for analyzing and improving writing.

Everything here *analyzes* text and *reports* findings. Nothing generates or
rewrites prose — the writer stays in control of every word.
"""

from . import grammar, literary, loaders, report, spelling, style
from .findings import Finding

__version__ = "0.2.0"
__all__ = [
    "grammar",
    "literary",
    "loaders",
    "report",
    "spelling",
    "style",
    "Finding",
    "__version__",
]
