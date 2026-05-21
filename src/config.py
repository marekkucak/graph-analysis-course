"""
Central configuration module for the Graph Masterclass.

Handles environment variables, paths, Neo4j connections, and global settings.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration for the learning environment."""

    # Project root directory
    PROJECT_ROOT = Path(__file__).parent.parent

    # Data directories
    DATA_DIR = PROJECT_ROOT / "data"
    DATA_SEED_DIR = DATA_DIR / "seed"
    DATA_GENERATED_DIR = DATA_DIR / "generated"
    DATA_PROCESSED_DIR = DATA_DIR / "processed"

    # Notebook and report directories
    NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
    REPORTS_DIR = PROJECT_ROOT / "reports"
    REPORTS_GENERATED_DIR = REPORTS_DIR / "generated"
    REPORTS_TEMPLATES_DIR = REPORTS_DIR / "templates"

    # Source directories
    SRC_DIR = PROJECT_ROOT / "src"
    CYPHER_DIR = PROJECT_ROOT / "cypher"

    # Random seed for reproducibility
    RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))

    # Neo4j configuration
    NEO4J_ENABLED = os.getenv("NEO4J_ENABLED", "false").lower() == "true"
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password_here")

    # Development settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def get_dataset_dir(cls, dataset_name: str) -> Path:
        """Get the directory for a specific generated dataset."""
        dataset_dir = cls.DATA_GENERATED_DIR / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        return dataset_dir

    @classmethod
    def neo4j_driver(self) -> Optional[object]:
        """Create and return a Neo4j driver if enabled.

        Returns:
            Driver object or None if Neo4j is not enabled.
        """
        if not self.NEO4J_ENABLED:
            return None

        try:
            from neo4j import GraphDatabase

            return GraphDatabase.driver(
                self.NEO4J_URI,
                auth=(self.NEO4J_USERNAME, self.NEO4J_PASSWORD),
            )
        except ImportError:
            print("Warning: neo4j module not installed. Neo4j features unavailable.")
            return None

    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        for directory in [
            cls.DATA_DIR,
            cls.DATA_SEED_DIR,
            cls.DATA_GENERATED_DIR,
            cls.DATA_PROCESSED_DIR,
            cls.NOTEBOOKS_DIR,
            cls.REPORTS_DIR,
            cls.REPORTS_GENERATED_DIR,
            cls.REPORTS_TEMPLATES_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
