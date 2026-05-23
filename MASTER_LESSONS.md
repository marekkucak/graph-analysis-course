# Master Lessons — Complete Learning Path

**Graph Masterclass — Full Curriculum Overview**

This document maps the complete 19-lesson path with objectives, prerequisites, and expected outcomes.

---

## Part I — Graph Foundations (Lessons 0-3)

### Lesson 00 — Environment Check
**Objective**: Verify local setup works  
**Duration**: 15 minutes  
**Prerequisites**: None  
**Key Outcomes**:
- Confirm all packages installed
- Understand Python-only vs Neo4j modes
- Know how to troubleshoot

**Notebook**: `notebooks/00_environment_check.ipynb`

---

### Lesson 01 — Graph Thinking and Graph Shapes
**Objective**: Understand what graphs are and how structure matters  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 00  
**Key Concepts**:
- Nodes, edges, directed/undirected
- Graph shapes (chain, star, ring, complete, bipartite)
- How structure affects algorithms

**Key Outcomes**:
- Recognize graph patterns in real problems
- Understand that "same nodes, different structure" → different algorithms
- Know when graphs are useful

**Datasets**: In-notebook toy graphs  
**Notebook**: `notebooks/01_graph_thinking_and_shapes.ipynb`

**Student Exercises**:
- Create graphs representing approval chains
- Identify risks in different graph structures
- Explain why graph shape matters

---

### Lesson 02 — NetworkX Foundations
**Objective**: Learn practical graph construction in Python  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 01  
**Key Concepts**:
- Graph construction from relational data
- Node and edge attributes
- Filtering and subgraphs
- Import/export formats

**Key Outcomes**:
- Build graphs from CSV data
- Add and access attributes
- Filter nodes and edges
- Export for visualization/sharing

**Datasets**: Small support ticket dataset (20 customers, 50 tickets)  
**Data Generation**: `src/data_generation/support_escalation.py`  
**Notebook**: `notebooks/02_networkx_foundations.ipynb`

**Student Exercises**:
- Add new node types to existing graph
- Create subgraph filtered by condition
- Export graph and reimport it

---

### Lesson 03 — Graph Profiling and Basic Metrics
**Objective**: Learn to inspect and understand graph structure before algorithms  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 02  
**Key Concepts**:
- Node count, edge count, density
- Degree distribution
- Connected components
- Isolates and bridges
- Clustering coefficient

**Key Outcomes**:
- Generate graph profiles automatically
- Visualize degree distributions
- Find anomalies (isolates, dense clusters)
- Understand what metrics mean

**Datasets**: Document-policy graph (100 docs, 15 topics, 300 edges)  
**Data Generation**: `src/data_generation/document_policy.py`  
**Notebook**: `notebooks/03_graph_profiling_metrics.ipynb`

**Student Exercises**:
- Find isolated documents
- Identify dense document clusters
- Detect ownerless critical documents
- Write value-discovery note on why profiling matters

---

## Part II — Core Graph Algorithms (Lessons 4-8)

### Lesson 04 — Centrality Algorithms
**Objective**: Understand different meanings of "importance" in graphs  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 03  
**Key Concepts**:
- Degree centrality (many connections)
- Betweenness centrality (lies on paths)
- Closeness centrality (can reach others quickly)
- PageRank (important because connected to important nodes)
- Eigenvector centrality (influence through neighbors)

**Key Outcomes**:
- Compute multiple centrality measures
- Rank nodes by different definitions of importance
- Interpret why top-degree ≠ most strategic
- Find bottlenecks and experts

**Datasets**: Hidden expert network (escalation patterns)  
**Data Generation**: `src/data_generation/hidden_experts.py`  
**Notebook**: `notebooks/04_centrality_algorithms.ipynb`

**Student Exercises**:
- Find most overloaded expert
- Identify best cross-team broker
- Compare degree vs PageRank rankings
- Explain bottlenecks in approval flows

---

### Lesson 05 — Community Detection
**Objective**: Find natural groups and clusters in graphs  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 04  
**Key Concepts**:
- Modularity optimization
- Greedy modularity (fast)
- Community quality metrics
- Overlapping vs non-overlapping communities

**Key Outcomes**:
- Detect communities automatically
- Evaluate community quality
- Understand when communities form naturally
- Identify bridge nodes between communities

**Datasets**: Organizational network  
**Data Generation**: `src/data_generation/approval_handoffs.py`  
**Notebook**: `notebooks/05_community_detection.ipynb`

**Student Exercises**:
- Run community detection on approval graph
- Identify inter-community bridges
- Evaluate modularity before/after merging teams
- Suggest reorganization based on communities

---

### Lesson 06 — Paths, Cycles, and Dependencies
**Objective**: Analyze paths and dependencies in networks  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 04  
**Key Concepts**:
- Shortest paths and Dijkstra algorithm
- All shortest paths
- Cycles and feedback loops
- Dependency chains
- Graph diameter

**Key Outcomes**:
- Find shortest routes through networks
- Detect circular dependencies
- Understand fragmentation via diameter
- Analyze impact of node removal (criticality)

**Datasets**: System dependency graph  
**Data Generation**: `src/data_generation/it_incidents.py`  
**Notebook**: `notebooks/06_paths_cycles_dependencies.ipynb`

**Student Exercises**:
- Find all paths between two systems
- Identify circular dependencies
- Analyze impact of critical system failure
- Optimize approval workflow for speed

---

### Lesson 07 — Similarity and Bipartite Graphs
**Objective**: Find similar entities and work with two-mode networks  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 05  
**Key Concepts**:
- Bipartite graphs (two node types)
- Node similarity based on neighborhoods
- Projections (reduce to single mode)
- Duplicate detection
- Recommendation logic

**Key Outcomes**:
- Identify similar users/products
- Detect duplicate records
- Project bipartite to recommendations
- Understand when similarity matters

**Datasets**: User-product or person-skill networks  
**Data Generation**: `src/data_generation/sales_accounts.py`  
**Notebook**: `notebooks/07_similarity_bipartite_graphs.ipynb`

**Student Exercises**:
- Find similar users by shared interests
- Detect duplicate customer records
- Generate product recommendations
- Explain why bipartite projection creates new edges

---

### Lesson 08 — Temporal and Process Graphs
**Objective**: Model and analyze graphs that change over time  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 06  
**Key Concepts**:
- Temporal graphs (time-dependent edges)
- Event sequences and process logs
- Process mining basics
- Time-windowed analysis
- Evolution metrics

**Key Outcomes**:
- Build temporal graphs from event logs
- Analyze process bottlenecks
- Detect anomalous patterns over time
- Understand process conformance

**Datasets**: Support ticket workflow  
**Data Generation**: `src/data_generation/support_escalation.py`  
**Notebook**: `notebooks/08_temporal_process_graphs.ipynb`

**Student Exercises**:
- Trace ticket resolution workflows
- Identify bottleneck states
- Detect unusual resolution patterns
- Optimize process time

---

## Part III — Neo4j and Graph Data Science (Lessons 9-13)

### Lesson 09 — Neo4j Property Graph Modeling
**Objective**: Model complex domains in Neo4j's property graph model  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 07  
**Requires**: Neo4j running (Docker)  
**Key Concepts**:
- Property graphs vs labeled graphs
- Multi-relationship modeling
- Graph schema design
- Constraints and indexes
- Loading data from CSV

**Key Outcomes**:
- Model complex business domains
- Create appropriate graph schema
- Load data efficiently
- Maintain data quality with constraints

**Datasets**: Multi-domain business graph  
**Cypher Scripts**: `cypher/00_constraints.cypher`, `cypher/01_load_*.cypher`  
**Notebook**: `notebooks/09_neo4j_property_graph_modeling.ipynb`

**Student Exercises**:
- Design graph schema for domain
- Create constraints for data quality
- Load multi-source data
- Query using Cypher basics

---

### Lesson 10 — Cypher Path Queries
**Objective**: Master path queries in Cypher for complex pattern matching  
**Duration**: 90 minutes  
**Prerequisites**: Lesson 09  
**Requires**: Neo4j running  
**Key Concepts**:
- Path matching syntax
- Variable-length paths
- Named paths
- Filtering during traversal
- Performance considerations

**Key Outcomes**:
- Write efficient path queries
- Find patterns of any length
- Combine path queries with graph algorithms
- Understand query optimization

**Notebook**: `notebooks/10_cypher_path_queries.ipynb`

**Student Exercises**:
- Find all approval paths
- Detect cycle in dependencies
- Calculate approval time by path length
- Optimize slow queries

---

### Lesson 11 — Neo4j Graph Data Science Workflow
**Objective**: Apply GDS algorithms at scale  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 10  
**Requires**: Neo4j + GDS plugin  
**Key Concepts**:
- GDS graph projections
- Algorithm catalog
- Stream vs write results
- Memory management
- Batching large operations

**Key Outcomes**:
- Project subgraphs for analysis
- Run PageRank, community detection, similarity
- Evaluate results
- Optimize for large graphs

**Notebook**: `notebooks/11_neo4j_gds_workflow.ipynb`

**Student Exercises**:
- Project multi-relationship graph
- Run PageRank and interpret
- Detect communities at scale
- Compare NetworkX vs GDS performance

---

### Lesson 12 — Graph Features for Machine Learning
**Objective**: Engineer graph features for ML models  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 11  
**Key Concepts**:
- Node features from centrality
- Structural features (clustering coefficient, triangles)
- Community membership features
- Neighborhood aggregation
- Feature engineering workflow

**Key Outcomes**:
- Create ML-ready feature sets from graphs
- Train models on graph features
- Evaluate feature importance
- Understand why graph features work

**Notebook**: `notebooks/12_graph_features_for_ml.ipynb`

**Student Exercises**:
- Engineer node features
- Train classification model
- Evaluate feature importance
- Interpret model decisions

---

### Lesson 13 — Embeddings and Link Prediction
**Objective**: Predict missing relationships using graph features and similarity metrics  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 12  
**Requires**: Neo4j running  
**Key Concepts**:
- Link prediction as supervised learning on node pairs
- Local similarity metrics (Jaccard, Adamic-Adar)
- Global GDS metrics (PageRank, degree, communities)
- Feature engineering for edge prediction
- Evaluation metrics for ranking (AUC, precision@k)
- Baseline vs. ML model comparison

**Key Outcomes**:
- Engineer features from graph structure for link prediction
- Train and compare ML models on edge prediction task
- Use AUC and ROC curves for ranking evaluation
- Interpret feature importance
- Deploy link prediction for business problems

**Datasets**: Document policy network (100 documents, 290 REFERENCES edges)  
**Data**: `data/seed/document_policy/` (CSV files)  
**Notebook**: `notebooks/13_embeddings_link_prediction.ipynb`

**Student Exercises**:
- Engineer new features (preferential attachment, PageRank product) for improved AUC
- Predict links on held-out documents (generalization test)
- Compare different similarity metrics (Jaccard vs. Pearson vs. Adamic-Adar)

**Real-World Applications**:
- Document recommendation systems
- Expert matching and ticket routing
- Knowledge graph completion
- Quality assurance (missing link detection)
- Cross-sell and supplier risk management

---

## Part IV — Advanced and Capstone (Lessons 14-19)

### Lesson 14 — GraphRAG and Evidence Graphs
**Objective**: Build evidence graphs for AI explainability and hierarchical retrieval-augmented generation  
**Duration**: 120 minutes  
**Prerequisites**: Lesson 13 (Link Prediction)  
**Key Concepts**:
- Evidence graph construction from relational data
- Entity extraction simulation
- Hierarchical community detection (Leiden algorithm)
- Evidence chain generation
- GraphRAG query system (vs. naive retrieval)
- Global sensemaking queries
- Path-based queries with community evidence ranking
- Pattern detection (bridge nodes, anomalies)
- Relevance scoring and ranking

**Key Outcomes**:
- Build evidence graphs with entity and relationship structures
- Apply hierarchical community detection (Level 0 coarse, Level 1 fine-grained)
- Compare naive keyword matching vs. hierarchical query ranking
- Understand comprehensiveness, diversity, and directness tradeoffs
- Generate community summaries for multi-level decision support
- Use community structure for evidence-based ranking
- Connect evidence graphs to link prediction (Lesson 13 integration)

**Datasets**: Document policy network (43 documents, 290 references)  
**Data**: `data/seed/document_policy/` (documents.csv, references.csv)  
**Data Generation**: `src/data_generation/document_policy.py`  
**Notebook**: `notebooks/14_graphrag_evidence_graphs.ipynb`

**Architecture Pattern**:
1. **Ingestion**: Extract entities and relationships from documents
2. **Graph Building**: Create directed graph with properties/descriptions
3. **Hierarchical Analysis**: Detect communities at multiple levels (Leiden algorithm)
4. **Summarization**: Generate summaries for each community
5. **Query Processing**: Compare naive vs. hierarchical ranking approaches
6. **Evidence Ranking**: Use community structure to rank and explain results

**Student Exercises**:
- **Exercise 1**: Build evidence graph from hidden_experts dataset with hierarchical community detection
- **Exercise 2**: Query hierarchy at different levels and observe precision vs. breadth tradeoff
- **Exercise 3**: Link prediction using community membership as ML features (bridge to Lesson 13)

**Real-World Applications**:
1. **Sales Account Expansion**: Discover cross-sell opportunities within customer communities
2. **IT Incident Blast Radius**: Understand failure propagation and system dependencies
3. **Compliance & Risk Evidence**: Build audit trails with multi-level evidence layers
4. **Hidden Experts Discovery**: Identify subject matter experts via bridge nodes connecting communities
5. **Scientific Literature Synthesis**: Extract research themes and detect emerging fields

**Key Insights**:
- **Comprehensiveness**: GraphRAG covers more communities than naive retrieval
- **Explainability**: Every result traces back to evidence (community → summary → entities)
- **Multi-level support**: Executives see communities, analysts see details
- **Global patterns**: Answer "what are the themes?" not just "find this entity"
- **Community features**: Modularity score, size, relationship density inform business decisions

**Comparison Matrix**:
| Dimension | Vector RAG | GraphRAG | Graph Algorithms |
|-----------|-----------|----------|-----------------|
| Query Speed | Fast | Slower | Medium |
| Comprehensiveness | Medium | High | Medium |
| Explainability | Low | High | Medium |
| Global Patterns | Weak | Strong | Strong |
| Specific Lookups | Strong | Medium | Medium |

**How Lessons 12-14 Connect**:
- **Lesson 12** (Graph Features): Engineer features from graph structure
- **Lesson 13** (Link Prediction): Use community structure as strong edge predictor
- **Lesson 14** (Evidence Graphs): Apply hierarchical communities for explainability and global reasoning

**Testing Notes**:
- Tested in synthetic data mode (no Neo4j required)
- Uses NetworkX community detection (greedy_modularity_communities fallback)
- Python-louvain preferred if available for better performance
- All 33 cells execute end-to-end without errors
- Datasets verified: 43 documents, 290 references edges

---

## Capstone Projects (Lessons 15-19)

Each capstone applies all prior lessons to a complete business scenario.

### Lesson 15 — Capstone: Support Escalation Analysis
**Objective**: Diagnose support system bottlenecks and identify hidden experts using graph analysis  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-8 (foundational), optionally 9-13  
**Status**: ✓ Implemented and tested

**Key Concepts**:
- Build escalation network graphs from support data
- Identify bottleneck agents (high in-degree, overloaded)
- Find hidden experts via scoring: resolution rate, escalation patterns, betweenness
- Detect natural support teams via community detection
- Analyze escalation paths and failure patterns
- Generate actionable recommendations

**Key Outcomes**:
- Diagnose bottleneck agents using degree metrics and bottleneck scoring
- Identify hidden organizational experts from network position
- Discover natural team structures without org chart
- Recommend process redesign (skill-based routing, knowledge transfer, workload balancing)
- Create agent performance profiles with graph metrics

**Dataset**: Support escalation network (agents, tickets, escalations)  
**Data**: `data/seed/support_escalation/` (customers.csv, tickets.csv, escalations.csv, ticket_events.csv)  
**Data Generation**: `src/data_generation/support_escalation.py`  
**Notebook**: `notebooks/15_capstone_support_escalation.ipynb`

**Analysis Flow**:
1. Load support data and build escalation network
2. Profile network: density, degree distribution, connectivity
3. Calculate bottleneck scores: escalations received / own tickets
4. Find bridge agents via betweenness centrality
5. Detect communities: natural support teams
6. Score hidden experts: resolution rate + escalation pattern + network position
7. Visualize: bottlenecks, experts, team structure, network graph
8. Generate recommendations: redistribution, knowledge transfer, rebalancing

**Student Challenge**:
- Can you predict which agents will burn out in 90 days?
- How would you redesign the escalation routing to reduce bottleneck load by 30%?
- What metrics would you monitor to prevent hidden experts from leaving?

**Real-World Applications**:
- Support team optimization and process redesign
- Expert identification for knowledge transfer programs
- Burnout prevention and workload balancing
- Skill-based team formation
- Performance and career development planning

---

### Lesson 16 — Capstone: Approval Handoff Optimization
**Objective**: Optimize approval processes  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-11  
**Dataset**: Multi-step approval workflows  
**Deliverable**: Recommended process redesign with time savings

**Notebook**: `notebooks/16_capstone_approval_handoffs.ipynb`

---

### Lesson 17 — Capstone: Hidden Experts Discovery
**Objective**: Identify key knowledge holders  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-5, 9-11  
**Dataset**: Collaboration and escalation patterns  
**Deliverable**: Organization chart of experts with impact assessment

**Notebook**: `notebooks/17_capstone_hidden_experts.ipynb`

---

### Lesson 18 — Capstone: Supplier Risk Analysis
**Objective**: Assess supply chain concentration risk  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-8  
**Dataset**: Multi-tier supplier network  
**Deliverable**: Risk assessment with dependency analysis

**Notebook**: `notebooks/18_capstone_supplier_risk.ipynb`

---

### Lesson 19 — Capstone: Portfolio Benchmark
**Objective**: Benchmark corporate portfolio  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-13  
**Dataset**: Multi-company financial and network data  
**Deliverable**: Peer comparison analysis with strategic insights

**Notebook**: `notebooks/19_capstone_portfolio_benchmark.ipynb`

---

## Learning Pathways

### Path A: Graph Foundations Only (8 hours)
For analysts who want core graph knowledge:
→ Lessons 0, 1, 2, 3, 4, 5, 6, 7, 8

**Outcome**: Understand graph analysis, run local algorithms, find patterns

---

### Path B: Full Stack (20 hours)
For engineers building graph systems:
→ Lessons 0-14 (all foundations + Neo4j + GDS)

**Outcome**: Design, build, query, and analyze production graphs

---

### Path C: Applied ML (16 hours)
For ML engineers working with graphs:
→ Lessons 0-8 (foundations), 12, 13, 15-19 (ML + capstones)

**Outcome**: Build ML models using graph features and predictions

---

### Path D: Business Analytics (12 hours)
For consultants and analysts:
→ Lessons 0-8 (foundations), 15-19 (capstones)

**Outcome**: Diagnose business problems using graph thinking

---

## Success Criteria

### For Each Lesson
- [ ] Concept understood (can explain to a peer)
- [ ] Notebook runs top-to-bottom
- [ ] Exercises completed with correct interpretation
- [ ] Value discovery note written

### For Course Completion
- [ ] All lessons in chosen path completed
- [ ] At least 2 capstone projects done
- [ ] One custom dataset analyzed end-to-end
- [ ] Can explain when and why to use graphs

---

**Start**: Lesson 00  
**Questions?**: Check Quick Reference guides in `/docs/`  
**Datasets**: Generated on-demand in notebooks  
**Estimated Total Time**: 8-20 hours depending on path
