"""
Graph construction and visualization utilities.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import Dict, Tuple, Any, Optional

import numpy as np


def describe_graph(G: nx.Graph) -> Dict[str, Any]:
    """Generate a comprehensive profile of a graph.

    Args:
        G: NetworkX graph object

    Returns:
        Dictionary with graph metrics
    """
    metrics = {
        "name": G.name if hasattr(G, "name") else "Unnamed",
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "density": nx.density(G),
        "is_directed": isinstance(G, nx.DiGraph),
        "is_weighted": nx.is_weighted(G),
    }

    # Node statistics
    if G.number_of_nodes() > 0:
        degrees = [G.degree(n) for n in G.nodes()]
        metrics["avg_degree"] = np.mean(degrees)
        metrics["min_degree"] = int(np.min(degrees))
        metrics["max_degree"] = int(np.max(degrees))

    # Connectivity
    if isinstance(G, nx.DiGraph):
        metrics["weakly_connected_components"] = nx.number_weakly_connected_components(G)
        metrics["strongly_connected_components"] = nx.number_strongly_connected_components(G)
    else:
        metrics["connected_components"] = nx.number_connected_components(G)

    # Isolates
    isolates = list(nx.isolates(G))
    metrics["isolates"] = len(isolates)

    # Clustering (only for undirected)
    if not isinstance(G, nx.DiGraph):
        try:
            metrics["avg_clustering_coefficient"] = nx.average_clustering(G)
        except:
            metrics["avg_clustering_coefficient"] = None

    return metrics


def plot_graph(
    G: nx.Graph,
    title: str = "Graph Visualization",
    figsize: Tuple[int, int] = (12, 8),
    layout: str = "spring",
    node_color: str = "lightblue",
    node_size: int = 300,
    edge_color: str = "gray",
    show_labels: bool = True,
    **kwargs
) -> None:
    """Visualize a NetworkX graph.

    Args:
        G: NetworkX graph object
        title: Title for the plot
        figsize: Figure size tuple (width, height)
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai', 'spring_shell')
        node_color: Color for nodes
        node_size: Size of nodes
        edge_color: Color for edges
        show_labels: Whether to show node labels
        **kwargs: Additional arguments passed to drawing functions
    """
    plt.figure(figsize=figsize)

    # Choose layout algorithm
    if layout == "spring":
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "spring_shell":
        pos = nx.shell_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42)

    # Draw network
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=node_color,
        node_size=node_size,
        **kwargs
    )
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, alpha=0.6, **kwargs)

    if show_labels:
        nx.draw_networkx_labels(G, pos, font_size=8, **kwargs)

    plt.title(title, fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def add_typed_node(
    G: nx.Graph,
    node_id: Any,
    node_type: str,
    **attrs
) -> None:
    """Add a typed node to a graph.

    Args:
        G: NetworkX graph
        node_id: Node identifier
        node_type: Type label for the node
        **attrs: Additional node attributes
    """
    attrs["node_type"] = node_type
    G.add_node(node_id, **attrs)


def add_typed_edge(
    G: nx.Graph,
    src: Any,
    dst: Any,
    rel_type: str,
    **attrs
) -> None:
    """Add a typed edge to a graph.

    Args:
        G: NetworkX graph
        src: Source node
        dst: Destination node
        rel_type: Relationship type label
        **attrs: Additional edge attributes
    """
    attrs["relationship_type"] = rel_type
    G.add_edge(src, dst, **attrs)


def filter_nodes_by_type(G: nx.Graph, node_type: str) -> nx.Graph:
    """Create a subgraph with only nodes of a specific type.

    Args:
        G: Original graph
        node_type: Type of nodes to include

    Returns:
        Subgraph with filtered nodes
    """
    filtered_nodes = [
        n for n, attrs in G.nodes(data=True)
        if attrs.get("node_type") == node_type
    ]
    return G.subgraph(filtered_nodes).copy()


def filter_edges_by_type(G: nx.Graph, rel_type: str) -> nx.Graph:
    """Create a subgraph with only edges of a specific relationship type.

    Args:
        G: Original graph
        rel_type: Relationship type to include

    Returns:
        Subgraph with filtered edges
    """
    filtered_edges = [
        (u, v) for u, v, attrs in G.edges(data=True)
        if attrs.get("relationship_type") == rel_type
    ]
    subgraph = G.edge_subgraph(filtered_edges).copy()
    return subgraph


def graph_to_edgelist(
    G: nx.Graph,
    filepath: str,
    include_attributes: bool = True
) -> None:
    """Export graph to edge list file.

    Args:
        G: NetworkX graph
        filepath: Output file path
        include_attributes: Whether to include edge attributes
    """
    nx.write_edgelist(
        G,
        filepath,
        data=include_attributes
    )


def graph_to_graphml(G: nx.Graph, filepath: str) -> None:
    """Export graph to GraphML format.

    Args:
        G: NetworkX graph
        filepath: Output file path
    """
    nx.write_graphml(G, filepath)


def graph_from_edgelist(
    filepath: str,
    directed: bool = False,
    encoding: str = "utf-8"
) -> nx.Graph:
    """Import graph from edge list file.

    Args:
        filepath: Input file path
        directed: Whether to create a directed graph
        encoding: File encoding

    Returns:
        Loaded NetworkX graph
    """
    if directed:
        return nx.read_edgelist(filepath, create_using=nx.DiGraph())
    else:
        return nx.read_edgelist(filepath)


def centrality_comparison_table(G: nx.Graph) -> Dict[str, Dict[str, float]]:
    """Compute multiple centrality measures for all nodes.

    Args:
        G: NetworkX graph

    Returns:
        Dictionary mapping node_id to centrality measures
    """
    results = {}

    # Degree centrality
    degree_cent = nx.degree_centrality(G)

    # Betweenness centrality
    between_cent = nx.betweenness_centrality(G)

    # Closeness centrality
    try:
        close_cent = nx.closeness_centrality(G)
    except:
        close_cent = {}

    # PageRank
    pagerank = nx.pagerank(G)

    # Eigenvector centrality (only for connected components in undirected graphs)
    try:
        eigen_cent = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        eigen_cent = {}

    for node in G.nodes():
        results[node] = {
            "degree": degree_cent.get(node, 0),
            "betweenness": between_cent.get(node, 0),
            "closeness": close_cent.get(node, 0),
            "pagerank": pagerank.get(node, 0),
            "eigenvector": eigen_cent.get(node, 0),
        }

    return results
