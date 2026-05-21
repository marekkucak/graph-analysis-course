"""
Data validation utilities.
"""

from typing import Any

import pandas as pd


def validate_dataframe(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """Validate that a DataFrame has required columns."""
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True


def validate_no_nulls(df: pd.DataFrame, columns: list[str] = None) -> bool:
    """Validate that specified columns have no null values."""
    cols_to_check = columns if columns else df.columns
    nulls = df[cols_to_check].isnull().sum()
    if nulls.sum() > 0:
        raise ValueError(f"Found null values:\n{nulls[nulls > 0]}")
    return True


def validate_unique_ids(df: pd.DataFrame, id_column: str) -> bool:
    """Validate that an ID column contains unique values."""
    if df[id_column].duplicated().any():
        raise ValueError(f"Duplicate IDs found in column '{id_column}'")
    return True


def validate_column_types(
    df: pd.DataFrame, expected_types: dict[str, Any]
) -> bool:
    """Validate column types match expected types."""
    for col, expected_type in expected_types.items():
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")
        if not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
            raise TypeError(
                f"Column '{col}' has type {df[col].dtype}, expected {expected_type}"
            )
    return True
