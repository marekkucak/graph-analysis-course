"""
Input/output utilities for reading and writing data files.
"""

from pathlib import Path
from typing import Any

import pandas as pd


def read_csv(filepath: Path, **kwargs) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    return pd.read_csv(filepath, **kwargs)


def write_csv(df: pd.DataFrame, filepath: Path, **kwargs) -> None:
    """Write a DataFrame to CSV."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, **kwargs)


def read_parquet(filepath: Path, **kwargs) -> pd.DataFrame:
    """Read a Parquet file into a DataFrame."""
    return pd.read_parquet(filepath, **kwargs)


def write_parquet(df: pd.DataFrame, filepath: Path, **kwargs) -> None:
    """Write a DataFrame to Parquet."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filepath, **kwargs)


def write_json(data: Any, filepath: Path, **kwargs) -> None:
    """Write data to JSON file."""
    import json

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, **kwargs)


def read_json(filepath: Path) -> Any:
    """Read JSON file."""
    import json

    with open(filepath, "r") as f:
        return json.load(f)
