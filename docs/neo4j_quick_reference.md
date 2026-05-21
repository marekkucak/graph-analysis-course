# Neo4j Quick Reference

## Connection & Authentication

```python
from neo4j import GraphDatabase

# Create driver
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

# Create session
session = driver.session()

# Close when done
session.close()
driver.close()
```

## Basic Cypher Queries

### Nodes and Properties

```cypher
// Create node
CREATE (n:Label {property: value})

// Get all nodes of type
MATCH (n:Label) RETURN n

// Get with filters
MATCH (n:Label) WHERE n.property = value RETURN n

// Create relationship
CREATE (a)-[r:RELATIONSHIP {property: value}]->(b)
```

### Common Patterns

```cypher
// Find connected nodes
MATCH (a:Label1)-[r]->(b:Label2) RETURN a, r, b

// Find paths
MATCH p = (a)-[*]-(b) RETURN p

// Find patterns
MATCH (a)-[:FOLLOWS]->(b)-[:FOLLOWS]->(c) RETURN a, b, c

// Count relationships
MATCH (a)-[r:TYPE]->(b) RETURN count(r)
```

### Aggregation

```cypher
// Group and count
MATCH (n:Label) RETURN n.property, count(*) as count

// Sort
MATCH (n:Label) RETURN n ORDER BY n.property DESC LIMIT 10

// Sum
MATCH (n:Label) RETURN sum(n.value) as total
```

## Neo4j Graph Data Science (GDS)

### Project Graph

```cypher
CALL gds.graph.project(
    'my-graph',
    'Node',
    'RELATIONSHIP'
)
```

### PageRank

```cypher
CALL gds.pagerank.stream('my-graph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name as node, score
ORDER BY score DESC
```

### Community Detection (Louvain)

```cypher
CALL gds.louvain.stream('my-graph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name as node, communityId
```

### Centrality (Betweenness)

```cypher
CALL gds.betweenness.stream('my-graph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name as node, score
ORDER BY score DESC
```

### Node Similarity

```cypher
CALL gds.nodeSimilarity.stream('my-graph')
YIELD node1Id, node2Id, similarity
WHERE similarity > 0.5
RETURN gds.util.asNode(node1Id).name as node1,
       gds.util.asNode(node2Id).name as node2,
       similarity
```

### Shortest Path

```cypher
CALL gds.shortestPath.dijkstra.stream('my-graph',
    {sourceNode: sourceNodeId, targetNode: targetNodeId}
)
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs
RETURN index, totalCost, nodeIds
```

## Loading Data from CSV

```cypher
// Load nodes
LOAD CSV WITH HEADERS FROM "file:///data.csv" as row
CREATE (n:Label {id: row.id, name: row.name})

// Load relationships
LOAD CSV WITH HEADERS FROM "file:///relationships.csv" as row
MATCH (a:Label1 {id: row.from})
MATCH (b:Label2 {id: row.to})
CREATE (a)-[r:TYPE {property: row.property}]->(b)
```

## Indexes and Constraints

```cypher
// Create index
CREATE INDEX FOR (n:Label) ON (n.property)

// Create constraint
CREATE CONSTRAINT FOR (n:Label) REQUIRE n.id IS UNIQUE

// Delete index
DROP INDEX index_name

// List indexes
SHOW INDEXES
```

## Performance Tips

- Use `RETURN DISTINCT` to avoid duplicates
- Use `LIMIT` to reduce result sets
- Build indexes on frequently queried properties
- Use `EXPLAIN` to preview query plan
- Use `PROFILE` to see actual performance

## Neo4j Browser Tips

- `:help` — Show help
- `:clear` — Clear history
- `:style` — Customize visualization
- `:params` — Set query parameters
- `$param` — Use parameter in query
