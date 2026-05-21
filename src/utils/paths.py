"""
Utility module for path operations and data directory management.
"""

from pathlib import Path

from src.config import Config


def get_data_path(dataset_name: str, filename: str) -> Path:
    """Get the full path to a data file in a dataset directory."""
    return Config.get_dataset_dir(dataset_name) / filename


def get_processed_path(filename: str) -> Path:
    """Get a path in the processed data directory."""
    Config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    return Config.DATA_PROCESSED_DIR / filename


def get_report_path(filename: str) -> Path:
    """Get a path in the generated reports directory."""
    Config.REPORTS_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return Config.REPORTS_GENERATED_DIR / filename


def ensure_data_dir(dataset_name: str) -> Path:
    """Ensure a dataset directory exists and return its path."""
    return Config.get_dataset_dir(dataset_name)
