# NetworkX Quick Reference

## Graph Construction

```python
import networkx as nx

# Create graphs
G = nx.Graph()           # Undirected
G = nx.DiGraph()         # Directed
G = nx.MultiGraph()      # Multiple edges between nodes
G = nx.MultiDiGraph()    # Directed multigraph

# Add nodes
G.add_node(1)
G.add_nodes_from([1, 2, 3])
G.add_node(1, color='red', size=10)  # With attributes

# Add edges
G.add_edge(1, 2)
G.add_edges_from([(1, 2), (2, 3), (3, 4)])
G.add_edge(1, 2, weight=5, relation='friend')  # With attributes

# Remove nodes/edges
G.remove_node(1)
G.remove_nodes_from([1, 2, 3])
G.remove_edge(1, 2)
```

## Graph Access

```python
# Nodes
G.nodes()                    # All nodes
G.number_of_nodes()         # Count
G.degree()                  # Degree of all nodes
G.degree(1)                 # Degree of node 1
G.neighbors(1)              # Neighbors of node 1

# Edges
G.edges()                   # All edges
G.number_of_edges()         # Count
G[1][2]                     # Edge data between 1 and 2
G.has_edge(1, 2)           # Check edge existence

# Node/edge data
G.nodes[1]                  # Attributes of node 1
G.edges[1, 2]               # Attributes of edge (1, 2)
```

## Graph Algorithms

```python
# Centrality
nx.degree_centrality(G)
nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.eigenvector_centrality(G)
nx.pagerank(G)

# Community detection
nx.community.greedy_modularity_communities(G)

# Paths
nx.shortest_path(G, source=1, target=2)
nx.shortest_path_length(G, source=1, target=2)
nx.all_shortest_paths(G, source=1, target=2)

# Connectivity
nx.is_connected(G)
nx.connected_components(G)
nx.number_connected_components(G)

# Clustering
nx.clustering(G)
nx.average_clustering(G)
nx.triangles(G)

# Density
nx.density(G)

# Diameter
nx.diameter(G)
```

## Subgraphs and Filtering

```python
# Subgraph
subgraph = G.subgraph([1, 2, 3])
subgraph = G.subgraph_view(filter_node=lambda n: G.degree(n) > 2)

# Copy
G_copy = G.copy()
G_copy = G.subgraph([1, 2, 3]).copy()

# View
G.edge_subgraph([(1, 2), (2, 3)])
```

## Graph Properties

```python
# Check properties
nx.is_directed(G)
nx.is_multigraph(G)
nx.is_weighted(G)
nx.is_tree(G)
nx.is_connected(G)

# Traversals
nx.dfs_edges(G, source=1)
nx.bfs_edges(G, source=1)

# Components
nx.connected_components(G)
nx.weakly_connected_components(G)  # For directed
nx.strongly_connected_components(G)  # For directed
```

## Export/Import

```python
# Export
nx.write_gml(G, 'file.gml')
nx.write_graphml(G, 'file.graphml')
nx.write_edgelist(G, 'file.edgelist')
nx.write_adjlist(G, 'file.adjlist')
nx.write_gpickle(G, 'file.gpickle')

# Import
G = nx.read_gml('file.gml')
G = nx.read_graphml('file.graphml')
G = nx.read_edgelist('file.edgelist')
G = nx.read_adjlist('file.adjlist')
G = nx.read_gpickle('file.gpickle')
```

## Layout and Visualization

```python
import matplotlib.pyplot as plt

# Compute layout
pos = nx.spring_layout(G)
pos = nx.circular_layout(G)
pos = nx.kamada_kawai_layout(G)
pos = nx.shell_layout(G)

# Draw
nx.draw(G, pos)
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_labels(G, pos, font_size=10)

plt.show()
```
