"""
Random seed and reproducibility utilities.
"""

import random

import numpy as np
from faker import Faker

from src.config import Config


def set_random_seed(seed: int = None) -> int:
    """Set random seed for reproducibility across all libraries."""
    if seed is None:
        seed = Config.RANDOM_SEED

    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

    return seed


def get_random_seed() -> int:
    """Get the current configured random seed."""
    return Config.RANDOM_SEED


# Initialize with config seed on import
set_random_seed(Config.RANDOM_SEED)
