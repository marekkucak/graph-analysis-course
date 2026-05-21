"""
Pytest configuration and shared fixtures for all tests.
"""

import pytest
import tempfile
from pathlib import Path

import networkx as nx
import pandas as pd

from src.utils import set_random_seed


@pytest.fixture
def random_seed():
    """Fixture that ensures deterministic tests."""
    set_random_seed(42)
    return 42


@pytest.fixture
def temp_data_dir():
    """Fixture providing a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_graph():
    """Fixture providing a simple sample graph for testing."""
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    return G


@pytest.fixture
def sample_dataframe():
    """Fixture providing a sample DataFrame."""
    return pd.DataFrame({
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "value": [10, 20, 15, 30, 25],
        "category": ["A", "B", "A", "C", "B"]
    })


@pytest.fixture
def sample_directed_graph():
    """Fixture providing a simple directed graph."""
    G = nx.DiGraph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
    return G


@pytest.fixture
def sample_bipartite_graph():
    """Fixture providing a simple bipartite graph."""
    G = nx.Graph()
    # Left nodes: people, Right nodes: topics
    people = ["Alice", "Bob", "Charlie"]
    topics = ["Python", "Graphs", "ML"]

    for person in people:
        G.add_node(person, bipartite=0)
    for topic in topics:
        G.add_node(topic, bipartite=1)

    # Add edges
    G.add_edges_from([
        ("Alice", "Python"),
        ("Alice", "Graphs"),
        ("Bob", "Python"),
        ("Bob", "ML"),
        ("Charlie", "Graphs"),
        ("Charlie", "ML"),
    ])

    return G


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
