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
**Objective**: Optimize approval processes by identifying bottlenecks and redesigning workflows for speed  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-8 (foundational), optionally 9-11  
**Status**: ✓ Implemented and tested

**Key Concepts**:
- Build approval network graphs from person-to-person handoffs
- Identify bottleneck approvers (high in-degree, overloaded)
- Find critical decision nodes via betweenness centrality
- Analyze department-level approval dependencies and cross-dept flows
- Detect natural approval clusters via community detection
- Score optimization opportunities: automation, delegation, parallel approvals
- Generate actionable redesign recommendations with impact estimates

**Key Outcomes**:
- Diagnose approval bottlenecks using degree metrics and bottleneck scoring
- Identify critical decision-makers who block approval paths
- Discover natural approval clusters without org hierarchy
- Recommend process changes (automation, parallelization, delegation)
- Estimate time savings and implementation priority (quick wins vs. structural)
- Create department efficiency comparison and cross-dept dependency maps

**Dataset**: Approval handoff network (people, departments, approvals)  
**Data**: `data/seed/approval_handoffs/` (people.csv, departments.csv, approvals.csv, documents.csv)  
**Data Generation**: `src/data_generation/approval_handoffs.py`  
**Notebook**: `notebooks/16_capstone_approval_handoffs.ipynb`

**Analysis Flow**:
1. Load approval data and build directed approval network (person → person edges)
2. Profile network: density, degree distribution, connectivity
3. Calculate bottleneck scores: approvals received / approvals given
4. Find critical nodes via betweenness centrality (on paths)
5. Analyze departments: internal vs. external approvals, manager count, efficiency
6. Detect communities: natural approval groups and inter-cluster flows
7. Visualize: bottleneck distribution, criticality scores, dept efficiency, network
8. Identify optimization opportunities: automation candidates, delegation targets, parallel paths
9. Generate recommendations: priority ranking, impact estimates, implementation roadmap

**Student Challenge**:
- Can you identify which approvals are just rubber stamps vs. adding real value?
- What would happen if we removed the #1 bottleneck person? (criticality analysis)
- How would you redesign the approval process to cut cycle time in half?
- What departments have most dependencies on each other?

**Real-World Applications**:
- Approval workflow automation (eliminate low-value reviews)
- Manager workload analysis and burnout prevention
- Process redesign (parallel vs. sequential approvals)
- SLA optimization (reduce approval time)
- Delegation strategy (push decisions down org hierarchy)
- Organizational design and team restructuring based on natural clusters

---

---

### Lesson 17 — Capstone: Hidden Experts Discovery
**Objective**: Identify hidden organizational expertise using multi-metric centrality scoring and classify expert types  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-5 (foundational), optionally 9-11  
**Status**: ✓ Implemented and tested

**Key Concepts**:
- Build escalation network graphs from support/collaboration data
- Compute 5 centrality metrics (in-degree, betweenness, closeness, eigenvector, issue resolution)
- Score expertise using weighted composite metric (not just single centrality)
- Classify experts by type: BOTTLENECK, BRIDGE, INFLUENCER, OVERLOADED, SILOED
- Identify knowledge transfer targets, burnout risks, and underutilized expertise
- Assess organizational resilience and single points of failure
- Generate succession planning and knowledge transfer recommendations

**Key Outcomes**:
- Discover hidden experts not visible in org chart (bridges, influencers)
- Identify bottleneck gatekeepers blocking escalation paths
- Find siloed experts with underutilized knowledge
- Quantify burnout risk (overload + isolation combination)
- Assess org resilience via critical node analysis
- Generate actionable knowledge transfer and succession plans
- Create expert type profiles with specific retention/development strategies

**Dataset**: Hidden experts escalation network (teams, people, issues, escalations)  
**Data**: `data/seed/hidden_experts/` (teams.csv, people.csv, issues.csv, escalations.csv)  
**Data Generation**: `src/data_generation/hidden_experts.py`  
**Notebook**: `notebooks/17_capstone_hidden_experts.ipynb`

**Network Size**: 18 people across 5 teams, 180 weighted escalation edges, 150 issues, 5 intentional anomalies

**Analysis Flow**:
1. Load teams, people, issues, escalations; profile distributions by team/seniority
2. Build directed escalation graph with node attributes and weighted edges
3. Attach issue resolution metrics per person (count, avg severity handled)
4. Calculate basic network stats: density, degree distribution, team distribution
5. Compute 5 centrality metrics: in-degree, betweenness, closeness, eigenvector + issue resolution
6. Score experts: weighted composite (25% trust, 20% gatekeeper risk, 15% reach, 20% influence, 20% impact)
7. Classify by type: BOTTLENECK (high between + high in), BRIDGE (high close, low between), INFLUENCER (high eigen), OVERLOADED (high in), SILOED (high out, low in)
8. Detect communities via greedy modularity; compare to org structure
9. Visualize: expert position map (between vs in-degree), top experts, influence distribution, type breakdown
10. Generate recommendations: knowledge transfer targets, bottleneck mitigation, leverage hidden expertise, resilience score

**Student Challenge**:
- Can you predict who will burn out in 90 days? (Combine overload + low influence)
- What's the cost of losing the #1 bottleneck person? (Criticality analysis)
- How would you redesign escalation paths to reduce single points of failure?
- Which hidden expert is most underutilized? (Siloed analysis with highest out-degree)
- What happens if we remove PERSON_01 (the gatekeeper)?

**Real-World Applications**:
- **Succession planning**: Identify who to groom for critical roles
- **Knowledge transfer programs**: Target high-expertise, high-burnout-risk people
- **Org resilience**: Reduce dependency on bottleneck people
- **Team restructuring**: Use community detection to reorganize along natural lines
- **Burnout prevention**: Monitor overloaded experts and influencers
- **Mentorship pairing**: Match experts with juniors strategically
- **Career development**: Different pathways for different expertise types

**Key Insights**:
- **Expertise ≠ Position**: A junior can be the #1 expert (gatekeeper, bridge)
- **Multiple metrics matter**: Single centrality (e.g., in-degree) misses influencers, bridges
- **Type matters more than rank**: A BRIDGE is fundamentally different from BOTTLENECK (both high-score but different risks/actions)
- **Hidden vulnerability**: Siloed experts represent risk (knowledge loss) AND opportunity (untapped potential)
- **Resilience = redundancy**: Organizations need depth in critical expertise (at least 2 per type)

**Engineered Anomalies in Dataset** (for teaching):
- **PERSON_00** (Overloaded): High in-degree → bottleneck, burnout risk
- **PERSON_01** (Gatekeeper): High betweenness, low seniority → critical dependency on junior
- **PERSON_02** (Bridge): High closeness, cross-team → integrator, should be protected
- **PERSON_03** (Influencer): High eigenvector, connected to experts → opinion leader
- **PERSON_04** (Siloed): High out-degree, low in-degree → underutilized specialist

**Testing Notes**:
- Tested in synthetic data mode (no Neo4j required)
- All 4 CSVs load successfully: 5 teams, 18 people, 150 issues, 180 escalation edges
- Centrality metrics computed without errors
- Community detection finds 3-5 natural clusters
- Expert scoring and classification assigns all 18 people to types
- All 10 cells execute end-to-end
- 4-panel visualization renders correctly

---

---

### Lesson 18 — Capstone: Supplier Risk Analysis
**Objective**: Solve real supply chain problems using multi-layer graph analysis  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-8 (foundational)  
**Status**: ✓ Implemented and tested

**Key Concepts**:
- Build multi-layer supply chain networks (suppliers, BUs, categories, locations, products)
- Identify vendor consolidation opportunities via bipartite projection
- Find single points of failure using centrality on product-supplier paths
- Assess geopolitical risk exposure via geographic concentration analysis
- Resolve duplicate vendors using similarity metrics (Jaccard, sequence matching)
- Score vendor health via payment reliability temporal analysis
- Combine multiple risk signals for comprehensive resilience scoring

**Key Outcomes**:
- Discover $50-100k+ annual cost savings via vendor consolidation
- Identify critical suppliers threatening major revenue streams
- Quantify supply chain exposure to geopolitical disruption
- Detect and merge duplicate vendor records (data quality)
- Flag deteriorating suppliers before financial failure
- Create actionable recommendations with ROI and implementation timeline
- Build executive summary for board-level supply chain strategy

**Dataset**: Multi-tier supply chain network (500 suppliers, 8 BUs, 40 categories, 30 locations, 50 products)  
**Data**: `data/seed/supplier_risk/` (8 CSVs: suppliers, business_units, categories, contracts, invoices, locations, products, risk_events)  
**Data Generation**: `src/data_generation/supplier_risk.py`  
**Notebook**: `notebooks/18_capstone_supplier_risk.ipynb`

**Network Scale**: ~2,200 nodes, ~24,000 edges; bipartite + weighted + spatial

**5 Real Business Problems Solved**:
1. **Cost Reduction via Consolidation** (Problem 1): Find multiple BUs buying same category from different vendors → consolidate for volume discount
2. **Supply Chain Resilience** (Problem 2): Identify suppliers serving many critical products → single points of failure → quantify revenue at risk
3. **Geopolitical Risk** (Problem 3): Map supplier geographic concentration → identify exposure to trade/conflict disruption
4. **Data Quality** (Problem 4): Detect duplicate vendors (similar names) → consolidate contracts → reduce overhead
5. **Vendor Health** (Problem 5): Track payment reliability over time → flag deteriorating suppliers → early warning system

**Analysis Flow**:
1. Load 8 CSVs; profile supplier health, payment reliability, geographic concentration, risk events
2. Build multi-layer network: suppliers ↔ BUs (contracts), suppliers ↔ categories (supply), suppliers ↔ locations (geography), suppliers ↔ products (dependencies)
3. Risk dashboard: supplier status distribution, on-time payment rates, event frequency, geographic risk heatmap
4. **Problem 1 — Consolidation**: Bipartite projection (BU-Category-Supplier); find clusters where same BU buys same category from multiple suppliers
5. **Problem 2 — Criticality**: Centrality on product-supplier subgraph; rank suppliers by revenue-at-risk; identify dual-source gaps
6. **Problem 3 — Geopolitical**: Aggregate suppliers by location; calculate % spend in high-risk zones (score > 0.7) per category; risk heatmap
7. **Problem 4 — Duplicates**: Jaccard similarity on supplier names; find matches >60% similarity; estimate consolidation spend
8. **Problem 5 — Health**: Temporal analysis of invoices; on_time_payment rate by supplier; flag <75% reliability; correlate with risk events
9. **Visualizations**: 4-panel dashboard (geopolitical risk vs. spend, consolidation savings opportunities, supplier criticality ranking, vendor health)
10. **Executive Summary**: Top 5 recommendations with priority, impact, timeline, and ROI; total financial impact; implementation roadmap

**5 Intentional Data Risks** (for teaching):
- **Spend Fragmentation**: 3 BUs independently buy staffing → no volume discount, pay $150, $145, $160/hr
- **Single-Source Critical**: SUPP_0147 supplies 5+ products ($50M+ revenue) with no backup → 6-month sourcing lead time
- **Geopolitical Concentration**: 15% suppliers in Taiwan (risk_score=0.85); electronics category 60% Taiwan-dependent
- **Duplicate Vendors**: "Acme Inc", "ACME Corp", "Acme Corporation" appear as 3 separate vendors across BUs
- **Payment Defaults**: SUPP_0089, SUPP_0234 have 65% on-time rate vs. 95% normal; correlated with high risk_score

**Student Challenge**:
- Can you identify $50k savings without damaging supplier relationships?
- If SUPP_0147 fails tomorrow, which products halt and for how long?
- Design a nearshoring strategy to reduce Taiwan exposure from 60% to 30% in electronics category
- How many duplicate vendors are you unknowingly paying overhead for?
- Which suppliers are early-warning signals for failure (declining payment reliability + rising risk events)?

**Real-World Applications**:
- **Procurement Finance**: Cost reduction via consolidation and spend analytics
- **Supply Chain Risk Management**: Resilience planning, contingency sourcing, dual-source strategy
- **Geopolitical Risk Hedging**: Diversification strategy, nearshoring, trade compliance
- **Vendor Management**: Performance monitoring, health scoring, contract optimization
- **Master Data Management**: Duplicate detection, entity resolution, data quality assurance
- **Business Continuity**: Single points of failure analysis, backup supplier qualification
- **Strategic Sourcing**: Category rationalization, supplier tiering, risk-based segmentation

**Key Insights**:
- **Multi-layer thinking**: Single-layer network (just suppliers) misses consolidation and criticality patterns
- **Financial dimension**: Weight edges by contract value for impact-weighted analysis (not just counts)
- **Similarity matters**: Name similarity + behavioral patterns (payment reliability) reveal duplicates better than exact matching
- **Temporal signals**: Payment reliability degradation + risk events = early warning system
- **Holistic scoring**: No single metric captures risk (combine centrality + reliability + geography)

**Comparison to Other Capstones**:
| Capstone | Focus | Network Type | Graph Technique |
|----------|-------|--------------|-----------------|
| Lesson 15 (Escalation) | Organizational bottlenecks | Directed, weighted | Centrality, community |
| Lesson 16 (Approval) | Process optimization | Directed, weighted | Centrality, clustering |
| Lesson 17 (Experts) | Knowledge distribution | Directed, temporal | Multi-metric scoring, classification |
| **Lesson 18 (Supplier)** | **Financial + Risk** | **Bipartite + multi-layer + spatial** | **Projection + similarity + temporal** |

**Testing Notes**:
- Data generator creates 8 CSVs: 500 suppliers, 8 BUs, 40 categories, 1,500 contracts, 20,000 invoices, 30 locations, 50 products, 100 events
- All 10 cells execute end-to-end without errors
- Identifies 15+ consolidation opportunities with $100k+ total savings potential
- Detects 3-5 critical suppliers with single-source risk
- Maps geopolitical exposure (15% in high-risk zones as designed)
- Finds 50+ potential duplicate vendors via Jaccard >60% similarity
- Flags 5-10 at-risk suppliers with <75% on-time payment
- 4-panel visualization renders correctly with actionable insights

---

---

### Lesson 19 — Capstone: Portfolio Benchmark
**Objective**: Optimize corporate portfolio strategy using multi-layer graph analysis  
**Duration**: 120 minutes  
**Prerequisites**: Lessons 0-13 (foundational + intermediate)  
**Status**: ✓ Implemented and tested

**Key Concepts**:
- Build multi-layer product/customer/market/supplier networks
- Measure revenue concentration risk via centrality metrics
- Identify market coverage gaps via bipartite graph projections
- Discover cross-sell opportunities through common neighbor analysis
- Classify portfolio health using BCG matrix (stars, cows, dogs, questions)
- Map supply chain vulnerabilities via betweenness centrality
- Calculate financial impact and strategic value creation

**Key Outcomes**:
- Identify critical revenue drivers and concentration risks ($100M+ mitigation)
- Map market gaps and competitive positioning (unserved TAM quantification)
- Discover $50M+ cross-sell upsell opportunities
- Identify single-source supply vulnerabilities and resilience gaps
- Classify portfolio health across product lifecycle stages
- Generate strategic roadmap with $200M+ value creation (3-year impact)
- Create executive-ready portfolio optimization dashboard

**Dataset**: Corporate product portfolio ($4.3B revenue, 50 products, 300+ customers, 25 markets)  
**Data**: `data/seed/portfolio_benchmark/` (9 CSVs: products, customers, purchases, markets, suppliers, competitors, product_market_penetration, product_supplier_mapping, competitor_products)  
**Data Generation**: `src/data_generation/portfolio_benchmark.py`  
**Notebook**: `notebooks/19_capstone_portfolio_benchmark.ipynb`

**Network Scale**: ~425 primary nodes (products, customers, markets, suppliers, competitors), ~2,676 edges; multi-layer financial + competitive + supply networks

**5 Real Business Problems Solved**:
1. **Revenue Concentration Risk** (Problem 1): Which products drive majority of revenue? Single-product failure exposure? → Degree/strength centrality identifies critical revenue nodes
2. **Market Positioning & Gaps** (Problem 2): Are we in right markets? Missing high-growth opportunities? → Bipartite product-market projection reveals gaps; competitive overlap analysis
3. **Cross-Sell Opportunities** (Problem 3): Which customers could buy more? Which segments underserved? → Common neighbors analysis + path finding identifies $50M+ TAM
4. **Supply Chain Vulnerability** (Problem 4): Single-source supplier risk? Revenue exposure? → Betweenness centrality on product-supplier graph identifies critical dependencies
5. **Portfolio Health** (Problem 5): Which products are stars vs. dogs? Portfolio aging? → BCG matrix classification via lifecycle + growth + market share

**Analysis Flow**:
1. Load 9 CSVs; profile revenue, customer segments, market reach, supplier concentration
2. Build multi-layer network: products ↔ customers (revenue), products ↔ markets (penetration), products ← suppliers (dependencies), products ↔ competitors (positioning)
3. Risk dashboard: revenue concentration, customer concentration, market coverage, supplier criticality, lifecycle distribution
4. **Problem 1 — Concentration**: Degree/strength centrality on revenue graph; top 3 products = X% revenue; diversification opportunities
5. **Problem 2 — Market Positioning**: Bipartite product-market projection; community detection identifies market clusters; competitive overlap; TAM in unserved markets
6. **Problem 3 — Cross-Sell**: Common neighbors (customers buying A not B); segment-specific penetration gaps; $50M+ opportunity quantification
7. **Problem 4 — Supply Risk**: Product-supplier graph; betweenness centrality identifies bottlenecks; single-source risk assessment; revenue-at-risk calculation
8. **Problem 5 — Portfolio Health**: BCG matrix (growth vs. market share); lifecycle classification; revenue distribution across stars/cows/dogs; health score
9. **Visualizations**: 4-panel dashboard (revenue Pareto, market coverage heatmap, BCG matrix bubble chart, supplier criticality ranking)
10. **Executive Summary**: Top 5 strategic recommendations with priority, impact, timeline, ROI; financial impact summary ($200M+ value creation); 3-year strategic roadmap

**5 Intentional Data Risks** (for teaching):
- **Concentration Risk**: Top 3 products = 18% of $4.37B (concentration opportunity for growth)
- **Market Gaps**: 3 high-growth markets completely unserved; competitors 40-60% present (TAM quantification needed)
- **Segment Penetration Gap**: SMB segment 95% in Products 0-2 but only 10% in Product 3 ($50M upsell opportunity)
- **Single-Source Critical Supplier**: SUPP_00 manufactures 7 products ($200M+ revenue) with no backups (6-month lead time risk)
- **Portfolio Aging**: ~10% of products declining >10% YoY (harvest vs. growth-stage imbalance)

**Student Challenge**:
- Can you identify which 3 products should we focus investment on (stars) vs. divest (dogs)?
- What's the TAM we're missing by not serving 3 high-growth markets?
- Which customer segment has highest upsell potential and why?
- If SUPP_00 fails tomorrow, which products halt and what's revenue at risk?
- Design a portfolio optimization strategy to reduce concentration from current to <50% while growing revenue by $500M over 3 years.

**Real-World Applications**:
- **Portfolio Strategy**: Optimize product mix for profitability and growth
- **Market Analysis**: Identify TAM gaps and competitive threats
- **Customer Success**: Target high-value upsell/cross-sell opportunities by segment
- **Risk Management**: Supply chain resilience, single-source mitigation
- **Financial Planning**: Allocate R&D budget across stars/cows/questions/dogs
- **M&A Strategy**: Identify portfolio gaps that could be filled via acquisition
- **Strategic Planning**: 3-5 year roadmap balancing growth, profitability, and risk

**Key Insights**:
- **Multi-layer insight**: Single product-revenue view misses market position, supply risk, and cross-sell potential
- **Bipartite projections**: Customer-product projection reveals segment gaps; product-market projection reveals geographic opportunities
- **Financial dimensioning**: Weight edges by revenue/penetration % for impact-weighted analysis
- **Portfolio management**: BCG matrix (simple but powerful) outperforms rank-based sorting for strategic allocation
- **Risk scoring**: Combine multiple risk dimensions (concentration + supply + customer) for holistic resilience

**Comparison to Other Capstones**:
| Capstone | Domain | Focus | Network Type | Key Techniques |
|----------|--------|-------|--------------|----------------|
| Lesson 15 (Escalation) | Org. Structure | Process optimization | Directed, weighted | Centrality, community |
| Lesson 16 (Approval) | Org. Process | Bottleneck analysis | Directed, weighted | Centrality, clustering |
| Lesson 17 (Experts) | Knowledge Mgmt | Expert discovery | Directed, temporal | Multi-metric scoring |
| Lesson 18 (Supplier) | Supply Chain | Risk assessment | Multi-layer, spatial | Similarity, temporal |
| **Lesson 19 (Portfolio)** | **Strategic Planning** | **Value optimization** | **Multi-layer, financial** | **Centrality, projection, classification** |

**Testing Notes**:
- Data generator creates 9 CSVs: 50 products, 300 customers, 1,735 purchases, 25 markets, 30 suppliers, 20 competitors
- All 10 cells execute end-to-end without errors
- Network builds: ~425 nodes, ~2,676 edges
- Identifies $4.37B annual revenue across portfolio
- Detects top 3 products concentration, market gaps, cross-sell opportunities
- Revenue concentration analysis works correctly
- Market coverage heatmap renders properly
- BCG matrix classification functional (stars, cows, dogs, questions)
- Supplier criticality ranking identifies single-source risks
- Executive summary generates strategic recommendations with quantified value ($200M+)

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
