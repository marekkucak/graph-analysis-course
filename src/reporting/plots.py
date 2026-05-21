"""
Plotting and visualization utilities for graph analysis results.
"""

from typing import Dict, List, Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def plot_degree_distribution(
    G: nx.Graph,
    figsize: tuple = (10, 6),
    title: str = "Degree Distribution"
) -> None:
    """Plot the degree distribution of a graph.

    Args:
        G: NetworkX graph
        figsize: Figure size
        title: Plot title
    """
    degrees = [G.degree(n) for n in G.nodes()]

    plt.figure(figsize=figsize)
    plt.hist(degrees, bins=max(10, len(set(degrees))), edgecolor='black', alpha=0.7)
    plt.xlabel('Degree', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_component_distribution(
    G: nx.Graph,
    figsize: tuple = (10, 6),
) -> None:
    """Plot the distribution of connected component sizes.

    Args:
        G: NetworkX graph (undirected)
        figsize: Figure size
    """
    if isinstance(G, nx.DiGraph):
        components = list(nx.weakly_connected_components(G))
    else:
        components = list(nx.connected_components(G))

    component_sizes = sorted([len(c) for c in components], reverse=True)

    plt.figure(figsize=figsize)
    plt.bar(range(len(component_sizes)), component_sizes, edgecolor='black', alpha=0.7)
    plt.xlabel('Component Index', fontsize=12)
    plt.ylabel('Component Size (nodes)', fontsize=12)
    plt.title('Connected Component Size Distribution', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()


def plot_centrality_ranking(
    centralities: Dict[str, float],
    top_k: int = 10,
    figsize: tuple = (10, 6),
    title: str = "Top Centrality Nodes"
) -> None:
    """Plot a bar chart of top centrality nodes.

    Args:
        centralities: Dict mapping node to centrality score
        top_k: Number of top nodes to display
        figsize: Figure size
        title: Plot title
    """
    sorted_nodes = sorted(centralities.items(), key=lambda x: x[1], reverse=True)[:top_k]
    nodes, scores = zip(*sorted_nodes)

    plt.figure(figsize=figsize)
    plt.barh(range(len(nodes)), scores, edgecolor='black', alpha=0.7)
    plt.yticks(range(len(nodes)), nodes)
    plt.xlabel('Centrality Score', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def node_attribute_summary(
    G: nx.Graph,
    attribute: str
) -> pd.DataFrame:
    """Create a summary DataFrame of a node attribute across the graph.

    Args:
        G: NetworkX graph
        attribute: Node attribute name

    Returns:
        DataFrame with node attribute statistics
    """
    values = [attrs.get(attribute) for _, attrs in G.nodes(data=True)]
    values = [v for v in values if v is not None]

    if not values:
        return pd.DataFrame()

    summary = {
        'count': len(values),
        'unique': len(set(values)) if isinstance(values[0], (str, int)) else None,
        'mean': np.mean([v for v in values if isinstance(v, (int, float))]) if isinstance(values[0], (int, float)) else None,
        'min': min([v for v in values if isinstance(v, (int, float))]) if isinstance(values[0], (int, float)) else None,
        'max': max([v for v in values if isinstance(v, (int, float))]) if isinstance(values[0], (int, float)) else None,
    }

    return pd.DataFrame([summary])


def edge_attribute_summary(
    G: nx.Graph,
    attribute: str
) -> pd.DataFrame:
    """Create a summary DataFrame of an edge attribute.

    Args:
        G: NetworkX graph
        attribute: Edge attribute name

    Returns:
        DataFrame with edge attribute statistics
    """
    values = [attrs.get(attribute) for _, _, attrs in G.edges(data=True)]
    values = [v for v in values if v is not None]

    if not values:
        return pd.DataFrame()

    summary = {
        'count': len(values),
        'unique': len(set(values)) if isinstance(values[0], (str, int)) else None,
        'mean': np.mean([v for v in values if isinstance(v, (int, float))]) if isinstance(values[0], (int, float)) else None,
        'min': min([v for v in values if isinstance(v, (int, float))]) if isinstance(values[0], (int, float)) else None,
        'max': max([v for v in values if isinstance(v, (int, float))]) if isinstance(values[0], (int, float)) else None,
    }

    return pd.DataFrame([summary])
