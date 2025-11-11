"""Shared foundation layer for funding history tracking.

This package provides the data models and repository layer following the
Repository pattern (Variant 2) with a flat structure and utility functions.
"""

from funding_tracker.shared import models, repositories

__all__ = ["models", "repositories"]
