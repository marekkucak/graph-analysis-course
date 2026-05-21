"""
Common utilities for synthetic data generation across all datasets.

Provides framework for:
- Faker configuration
- Timestamp and time series generation
- Skewed distributions
- Ground truth injection
- Reproducibility
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import json

import numpy as np
import pandas as pd
from faker import Faker

from src.config import Config
from src.utils import set_random_seed, write_json


def initialize_faker(seed: int = None) -> Faker:
    """Initialize Faker instance with seed for reproducibility."""
    if seed is None:
        seed = Config.RANDOM_SEED
    fake = Faker()
    Faker.seed(seed)
    return fake


def generate_timestamps(
    n: int,
    start_date: str = "2023-01-01",
    end_date: str = "2024-12-31",
    seed: int = None
) -> List[datetime]:
    """Generate random timestamps within a date range.

    Args:
        n: Number of timestamps
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        seed: Random seed

    Returns:
        List of datetime objects
    """
    set_random_seed(seed)

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    timestamps = [start + timedelta(seconds=int(x)) for x in
                  np.random.randint(0, int((end - start).total_seconds()), n)]
    return sorted(timestamps)


def generate_skewed_values(
    n: int,
    distribution: str = "pareto",
    min_val: float = 1,
    max_val: float = 100,
    seed: int = None
) -> np.ndarray:
    """Generate skewed numeric values (80/20 distributions).

    Args:
        n: Number of values
        distribution: 'pareto', 'exponential', 'lognormal'
        min_val: Minimum value
        max_val: Maximum value
        seed: Random seed

    Returns:
        Array of skewed values
    """
    set_random_seed(seed)

    if distribution == "pareto":
        # Pareto distribution (heavy-tailed)
        values = np.random.pareto(1.5, n) + 1
    elif distribution == "exponential":
        values = np.random.exponential(scale=1, size=n)
    elif distribution == "lognormal":
        values = np.random.lognormal(mean=0, sigma=1, size=n)
    else:
        values = np.random.normal(loc=50, scale=15, size=n)

    # Normalize to range
    values = (values - values.min()) / (values.max() - values.min())
    values = values * (max_val - min_val) + min_val

    return np.clip(values, min_val, max_val)


def create_ground_truth_file(
    dataset_name: str,
    patterns: List[Dict[str, Any]],
    seed: int = None,
    filepath: str = None
) -> str:
    """Create a ground truth file for a synthetic dataset.

    Args:
        dataset_name: Name of dataset
        patterns: List of injected pattern descriptions
        seed: Random seed used
        filepath: Output file path (optional)

    Returns:
        Path to created file
    """
    if seed is None:
        seed = Config.RANDOM_SEED

    ground_truth = {
        "dataset": dataset_name,
        "seed": seed,
        "created_at": datetime.now().isoformat(),
        "injected_patterns": patterns
    }

    if filepath is None:
        from src.utils import get_data_path
        filepath = str(get_data_path(dataset_name, "ground_truth.json"))

    write_json(ground_truth, filepath, indent=2)
    return filepath


def inject_anomaly(
    df: pd.DataFrame,
    column: str,
    indices: List[int],
    values: List[Any]
) -> pd.DataFrame:
    """Inject anomalies into specific rows of a DataFrame.

    Args:
        df: Original DataFrame
        column: Column name to modify
        indices: Row indices to modify
        values: New values to inject

    Returns:
        Modified DataFrame
    """
    df_copy = df.copy()
    for idx, val in zip(indices, values):
        if idx < len(df_copy):
            df_copy.loc[idx, column] = val
    return df_copy


def create_data_split(
    df: pd.DataFrame,
    train_ratio: float = 0.7,
    seed: int = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split DataFrame into train/test sets.

    Args:
        df: Input DataFrame
        train_ratio: Proportion for training
        seed: Random seed

    Returns:
        Tuple of (train_df, test_df)
    """
    set_random_seed(seed)
    mask = np.random.rand(len(df)) < train_ratio
    return df[mask], df[~mask]


def sample_weighted(
    population: List[Any],
    n: int,
    weights: np.ndarray = None,
    seed: int = None
) -> List[Any]:
    """Sample from population with optional weights (skewed distribution).

    Args:
        population: List to sample from
        n: Number of samples
        weights: Optional weights (will be normalized)
        seed: Random seed

    Returns:
        Sampled list
    """
    set_random_seed(seed)

    if weights is None:
        weights = np.ones(len(population))

    weights = weights / weights.sum()  # Normalize
    return list(np.random.choice(population, size=n, p=weights))
