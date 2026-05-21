# Graph Algorithm Cheatsheet

## Centrality Measures

### Degree Centrality
- **What**: Number of direct connections
- **When**: Who is most connected?
- **Interpretation**: High = many neighbors
- **Use case**: Popularity, connectivity

```python
nx.degree_centrality(G)
```

### Betweenness Centrality
- **What**: How often a node lies on shortest paths
- **When**: Who is a broker or bottleneck?
- **Interpretation**: High = lies on many shortest paths
- **Use case**: Finding critical connectors, bridges

```python
nx.betweenness_centrality(G)
```

### Closeness Centrality
- **What**: Average distance to all other nodes
- **When**: Who can reach everyone quickly?
- **Interpretation**: High = short average path length
- **Use case**: Information diffusion, influence

```python
nx.closeness_centrality(G)
```

### PageRank
- **What**: Importance based on incoming connections from important nodes
- **When**: Who is important because of who connects to them?
- **Interpretation**: High = connected to other important nodes
- **Use case**: Ranking, web pages, authority

```python
nx.pagerank(G)
```

### Eigenvector Centrality
- **What**: Influence through influential neighbors
- **When**: Who has influential neighbors?
- **Interpretation**: High = neighbors are important
- **Use case**: Authority, influence networks

```python
nx.eigenvector_centrality(G)
```

## Community Detection

### Greedy Modularity Optimization
- **What**: Groups nodes into communities to maximize modularity
- **When**: Find natural clusters in graph
- **Parameter**: Weight (optional)
- **Result**: Set of node sets (communities)

```python
nx.community.greedy_modularity_communities(G)
```

### Louvain Method
- **What**: Multi-level optimization for large graphs
- **When**: Need fast community detection on large graphs
- **Requires**: python-louvain library

## Path Analysis

### Shortest Paths
- **What**: Minimum length path between nodes
- **When**: What's the shortest route?
- **Result**: List of nodes in path

```python
nx.shortest_path(G, 1, 5)          # Path from 1 to 5
nx.shortest_path_length(G, 1, 5)  # Length only
```

### All Shortest Paths
- **What**: All shortest paths between two nodes
- **When**: Multiple shortest routes exist?

```python
list(nx.all_shortest_paths(G, 1, 5))
```

### Longest Path / Diameter
- **What**: Longest shortest path in graph
- **When**: How fragmented is the network?

```python
nx.diameter(G)
```

## Graph Properties

### Density
- **What**: Proportion of possible edges present
- **Range**: 0 (sparse) to 1 (complete)
- **Interpretation**: Higher = more connected

```python
nx.density(G)  # edges / max_possible_edges
```

### Clustering Coefficient
- **What**: Tendency of neighbors to form triangles
- **Range**: 0 to 1
- **Interpretation**: High = tight clusters

```python
nx.clustering(G)            # Per node
nx.average_clustering(G)   # Whole graph
```

### Assortativity
- **What**: Do similar nodes connect to similar nodes?
- **Range**: -1 to 1
- **Interpretation**: Positive = assortative (like connects to like)

```python
nx.degree_assortativity_coefficient(G)
```

## Connectivity

### Connected Components
- **What**: Groups of nodes connected by path
- **Undirected graphs**:

```python
nx.is_connected(G)
nx.connected_components(G)
nx.number_connected_components(G)
```

### Directed Graphs:
```python
nx.is_weakly_connected(G)
nx.weakly_connected_components(G)
nx.is_strongly_connected(G)
nx.strongly_connected_components(G)
```

### Bridges
- **What**: Edges whose removal disconnects the graph
- **When**: What dependencies are critical?

```python
list(nx.bridges(G))
```

## Bipartite Graphs

### Check and Projects
```python
from networkx.algorithms import bipartite

bipartite.is_bipartite(G)
bipartite.sets(G)  # Partition into two sets

# Project to one partition
X = bipartite.projected_graph(G, nodes=set1)
```

### Bipartite Metrics
```python
bipartite.density(G, nodes=set1)
bipartite.linalg.biadjacency_matrix(G, X, Y)
```

## Summary Table

| Algorithm | Complexity | Use Case | Range |
|-----------|-----------|----------|-------|
| Degree centrality | O(n) | Popularity | 0-1 |
| Betweenness | O(n³) | Bottlenecks | 0-1 |
| Closeness | O(n²) | Reach | 0-1 |
| PageRank | O(n+e) | Authority | 0-1 |
| Eigenvector | O(n+e) | Influence | 0-1 |
| Modularity | O(e log n) | Communities | various |
| Shortest path | O(n+e) | Routes | int |
| Clustering | O(n²) | Cohesion | 0-1 |
| Density | O(1) | Sparsity | 0-1 |
