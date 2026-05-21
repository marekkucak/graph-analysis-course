# Graph Masterclass — Agent Build Specification

**Project codename:** `pe-graph-value-masterclass`  
**Primary goal:** teach graph thinking, graph analytics, graph algorithms, and graph data science through runnable local notebooks.  
**Secondary context:** private-equity and corporate value discovery examples, used as realistic business scenarios for exercises.  
**Audience:** technically curious students, data analysts, AI engineers, forward-deployed AI engineers, operating partners, and consultants who want to learn graph approaches by building practical examples.  
**Output style:** clean, local, notebook-first learning environment. No heavy front end. No over-engineered app layer. Neo4j Browser and notebooks are enough.

---

## 0. Operating principles for the coding AI agent

You are the coding AI agent responsible for creating the full learning repo from this specification.

Your job is to build a **runnable graph learning environment** with:

1. Synthetic corporate datasets.
2. Jupyter notebooks.
3. NetworkX-based graph analytics.
4. Neo4j + Cypher examples.
5. Neo4j Graph Data Science examples where appropriate.
6. Optional PM4Py process-mining examples for event-log workflows.
7. Small, clear reports generated from notebooks.
8. No heavy UI unless explicitly requested later.

The masterclass is not primarily about PE consulting. The PE/corporate environment is the **story layer** used to make graph problems realistic:

```text
primary learning goal: graphs, graph analytics, graph data science
secondary scenario layer: corporate value discovery in PE-backed companies
```

When implementing each lesson, always prioritize teaching the graph method first:

```text
Graph concept → data model → algorithm → result interpretation → corporate example → AI/value note
```

Do not invert the focus into business consulting slides. This repo is a technical learning environment.

---

## 1. Target local development environment

The environment must run on a normal student laptop or workstation.

### 1.1 Required local tools

Use this default stack:

```text
Python 3.11+
JupyterLab
Pandas
NumPy
NetworkX
Matplotlib
PyVis
Faker
Scikit-learn
DuckDB
Neo4j Python driver
Graph Data Science Python client
PM4Py
python-dotenv
pytest
ruff
```

### 1.2 Optional local services

Use Docker Compose for services:

```text
Neo4j Community or Enterprise-compatible local container
Neo4j Graph Data Science plugin if available in the selected image
JupyterLab container optional, but local venv is acceptable
```

The repo should support two modes:

#### Mode A — Python-only mode

Used for the first half of the course and for students who do not want Neo4j yet.

```text
Pandas → NetworkX → notebook visualizations → CSV/parquet outputs
```

#### Mode B — Neo4j mode

Used for Cypher, persistent graph modeling, and GDS.

```text
Pandas/generated CSV → Neo4j load → Cypher queries → GDS algorithms → notebook interpretation
```

### 1.3 No heavy front end

Do not create React, FastAPI, dashboards, or web apps unless explicitly requested later.

Allowed lightweight output:

```text
Jupyter notebooks
Markdown reports
CSV/parquet outputs
Static PNG charts
PyVis HTML graph visualizations
Neo4j Browser queries
Optional Neo4j Bloom notes if available
```

---

## 2. Repository structure to generate

Create this repo structure:

```text
pe-graph-value-masterclass/
│
├── README.md
├── MASTER_LESSONS.md
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── .env.example
├── Makefile
│
├── data/
│   ├── seed/
│   ├── generated/
│   │   ├── support_escalation/
│   │   ├── approval_handoffs/
│   │   ├── hidden_experts/
│   │   ├── document_policy/
│   │   ├── supplier_risk/
│   │   ├── finance_reporting/
│   │   ├── project_margin/
│   │   ├── it_incidents/
│   │   ├── compliance_controls/
│   │   ├── sales_accounts/
│   │   ├── product_feedback/
│   │   └── portfolio_benchmark/
│   └── processed/
│
├── notebooks/
│   ├── 00_environment_check.ipynb
│   ├── 01_graph_thinking_and_shapes.ipynb
│   ├── 02_networkx_foundations.ipynb
│   ├── 03_graph_profiling_metrics.ipynb
│   ├── 04_centrality_algorithms.ipynb
│   ├── 05_community_detection.ipynb
│   ├── 06_paths_cycles_and_dependencies.ipynb
│   ├── 07_similarity_and_bipartite_graphs.ipynb
│   ├── 08_temporal_and_process_graphs.ipynb
│   ├── 09_neo4j_property_graph_modeling.ipynb
│   ├── 10_cypher_path_queries.ipynb
│   ├── 11_neo4j_gds_workflow.ipynb
│   ├── 12_graph_features_for_ml.ipynb
│   ├── 13_embeddings_and_link_prediction.ipynb
│   ├── 14_graphrag_evidence_graph_optional.ipynb
│   ├── 15_capstone_support_escalation.ipynb
│   ├── 16_capstone_approval_handoffs.ipynb
│   ├── 17_capstone_hidden_experts.ipynb
│   ├── 18_capstone_supplier_risk.ipynb
│   └── 19_capstone_portfolio_benchmark.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_generation/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── support_escalation.py
│   │   ├── approval_handoffs.py
│   │   ├── hidden_experts.py
│   │   ├── document_policy.py
│   │   ├── supplier_risk.py
│   │   ├── finance_reporting.py
│   │   ├── project_margin.py
│   │   ├── it_incidents.py
│   │   ├── compliance_controls.py
│   │   ├── sales_accounts.py
│   │   ├── product_feedback.py
│   │   └── portfolio_benchmark.py
│   │
│   ├── graph_builders/
│   │   ├── __init__.py
│   │   ├── networkx_builders.py
│   │   ├── bipartite.py
│   │   ├── process_graphs.py
│   │   └── neo4j_loaders.py
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── profiling.py
│   │   ├── centrality.py
│   │   ├── communities.py
│   │   ├── paths.py
│   │   ├── similarity.py
│   │   ├── process_mining.py
│   │   ├── ml_features.py
│   │   └── interpretation.py
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── markdown_reports.py
│   │   ├── tables.py
│   │   └── plots.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── paths.py
│       ├── io.py
│       ├── validation.py
│       └── random_seed.py
│
├── cypher/
│   ├── 00_constraints.cypher
│   ├── 01_load_support_escalation.cypher
│   ├── 02_load_approval_handoffs.cypher
│   ├── 03_load_hidden_experts.cypher
│   ├── 04_load_document_policy.cypher
│   ├── 05_load_supplier_risk.cypher
│   ├── 06_load_finance_reporting.cypher
│   ├── 07_load_project_margin.cypher
│   ├── 08_load_it_incidents.cypher
│   ├── 09_load_compliance_controls.cypher
│   ├── 10_load_sales_accounts.cypher
│   ├── 11_load_product_feedback.cypher
│   ├── 12_load_portfolio_benchmark.cypher
│   ├── gds_examples.cypher
│   └── query_library.cypher
│
├── reports/
│   ├── templates/
│   │   ├── lesson_report_template.md
│   │   ├── graph_findings_template.md
│   │   └── value_discovery_canvas.md
│   └── generated/
│
├── tests/
│   ├── test_data_generation.py
│   ├── test_graph_builders.py
│   ├── test_graph_metrics.py
│   └── test_synthetic_ground_truth.py
│
└── docs/
    ├── graph_algorithm_cheatsheet.md
    ├── graph_modeling_patterns.md
    ├── neo4j_quick_reference.md
    ├── networkx_quick_reference.md
    ├── process_graphs_quick_reference.md
    └── pe_corporate_use_case_map.md
```

---

## 3. Build commands

Create a `Makefile` with these targets:

```makefile
install:
	python -m pip install -U pip
	pip install -r requirements.txt

generate-data:
	python -m src.data_generation.support_escalation
	python -m src.data_generation.approval_handoffs
	python -m src.data_generation.hidden_experts
	python -m src.data_generation.document_policy
	python -m src.data_generation.supplier_risk
	python -m src.data_generation.finance_reporting
	python -m src.data_generation.project_margin
	python -m src.data_generation.it_incidents
	python -m src.data_generation.compliance_controls
	python -m src.data_generation.sales_accounts
	python -m src.data_generation.product_feedback
	python -m src.data_generation.portfolio_benchmark

jupyter:
	jupyter lab

neo4j-up:
	docker compose up -d neo4j

neo4j-down:
	docker compose down

test:
	pytest -q

lint:
	ruff check src tests

format:
	ruff format src tests

verify:
	make lint
	make test
```

---

## 4. Notebook design contract

Every notebook must follow the same teaching pattern.

### 4.1 Required notebook sections

Each notebook must contain these sections:

```text
1. Learning goal
2. Graph concept explained simply
3. Corporate example context
4. Dataset loaded or generated
5. Graph model
6. Build the graph
7. Basic graph profiling
8. Main algorithm or technique
9. Interpretation of results
10. Exercise tasks
11. Challenge extension
12. Value discovery note
13. Summary checklist
```

### 4.2 Required notebook style

Each notebook should be:

- Runnable from top to bottom.
- Deterministic with a fixed random seed.
- Short enough to complete in 30 to 90 minutes.
- Clear enough for self-study.
- Focused on one graph method or closely related family of methods.
- Written with explanatory Markdown between code cells.
- Not dependent on hidden external APIs.

### 4.3 Notebook cell conventions

Use these cell labels in Markdown headings:

```markdown
## Learning goal
## Business context
## Graph model
## Load data
## Build graph
## Inspect graph
## Run algorithm
## Interpret results
## Student exercise
## Challenge
## Value discovery note
## Summary
```

### 4.4 Result interpretation rule

Do not show an algorithm output without interpreting it.

Bad:

```text
Here are PageRank scores.
```

Good:

```text
The top PageRank nodes are not simply the most frequent nodes. They are connected to other important nodes. In this approval graph, the Legal Review node has high PageRank because many high-value approval paths flow through it, not just because it appears often.
```

---

## 5. Synthetic data generation principles

The masterclass should use synthetic data, but it must feel realistic.

### 5.1 General generation strategy

For every dataset:

1. Generate entity tables.
2. Generate relationship/event tables.
3. Inject hidden ground-truth problems.
4. Save the ground-truth injection file separately.
5. Build graph edges from the generated data.
6. Let the student rediscover the injected truth using graph analytics.

Example output files:

```text
data/generated/support_escalation/customers.csv
data/generated/support_escalation/tickets.csv
data/generated/support_escalation/ticket_events.csv
data/generated/support_escalation/agents.csv
data/generated/support_escalation/products.csv
data/generated/support_escalation/issues.csv
data/generated/support_escalation/knowledge_articles.csv
data/generated/support_escalation/ground_truth.json
```

### 5.2 Ground-truth injection file

Every dataset must include a `ground_truth.json` file.

Example:

```json
{
  "dataset": "support_escalation",
  "seed": 42,
  "injected_patterns": [
    {
      "id": "billing_api_escalation",
      "description": "Billing API timeout tickets escalate to engineering 75% of the time.",
      "expected_detection_methods": ["community_detection", "escalation_rate", "product_issue_bipartite_graph"],
      "expected_entities": ["Billing", "API timeout", "Engineering"]
    },
    {
      "id": "integration_expert_dependency",
      "description": "One engineer resolves 45% of integration escalations.",
      "expected_detection_methods": ["degree_centrality", "betweenness_centrality", "resolved_by_distribution"],
      "expected_entities": ["engineer_hidden_expert_01"]
    }
  ]
}
```

Students should not open `ground_truth.json` until the end of the exercise.

### 5.3 Data scale rules

Keep datasets small enough for a laptop.

Recommended limits:

```text
Small introductory notebooks: 50–500 nodes, 100–2,000 edges
Intermediate notebooks: 1,000–10,000 nodes, 5,000–50,000 edges
Neo4j/GDS notebooks: stay under memory-heavy workloads by default
Capstone datasets: configurable size with small default
```

### 5.4 Realism rules

Synthetic data should include:

- Realistic department names.
- Realistic roles.
- Realistic timestamps.
- Realistic process states.
- Skewed distributions, not uniform randomness.
- A few rare but important exceptions.
- Cost, time, value, risk, or revenue fields where appropriate.

Use skewed distributions because business graphs are rarely uniform. A few entities often dominate work, risk, cost, or influence.

### 5.5 LLM-assisted dummy data generation

Use LLMs only for semantic variety, not for final numeric consistency.

Good use of AI:

```text
Generate realistic issue names.
Generate role names.
Generate document titles.
Generate policy topic names.
Generate supplier categories.
Generate customer feedback text.
Generate short ticket descriptions.
```

Better handled by Python:

```text
row counts
timestamps
case durations
edge generation
probability distributions
injected ground truth
consistency of IDs
foreign keys
```

---

## 6. Core learning map

The masterclass should teach these graph capabilities in order:

```text
1. Graph thinking and graph shapes
2. Graph construction with NetworkX
3. Graph profiling and basic metrics
4. Centrality algorithms
5. Community detection
6. Path analysis, shortest paths, cycles, and dependencies
7. Bipartite graphs and projections
8. Similarity, duplicate detection, and recommendation
9. Temporal graphs and process graphs
10. Property graph modeling with Neo4j
11. Cypher path queries
12. Neo4j Graph Data Science workflow
13. Graph features for machine learning
14. Embeddings and link prediction
15. Optional GraphRAG evidence graph
16. Capstone business graph problems
```

---

# Part I — Graph Foundations with Python

---

## Lesson 00 — Environment check

### Goal

Verify that the local environment works before starting the course.

### Notebook

```text
notebooks/00_environment_check.ipynb
```

### Implementation tasks

The agent must create a notebook that checks:

```python
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sklearn
import faker
import duckdb
```

It should also check optional imports:

```python
import pm4py
from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
```

### Expected outputs

The notebook should print:

```text
Python version
Package versions
Current working directory
Data directory exists
Neo4j connection status if configured
```

### Acceptance criteria

- The notebook runs without Neo4j.
- If Neo4j credentials are not configured, it should show a friendly warning, not fail.
- It should explain how to proceed in Python-only mode.

---

## Lesson 01 — Graph thinking and graph shapes

### Goal

Teach the student what graphs are, when they are useful, and how different shapes behave.

### Primary graph concepts

```text
node
edge
relationship
property
directed graph
undirected graph
weighted graph
bipartite graph
multigraph
path
cycle
component
degree
density
```

### Corporate example context

Use small corporate examples only as illustrations:

```text
people communicating with people
tickets assigned to agents
documents referencing policies
requests moving through approval states
systems depending on systems
```

### Dataset

Generate tiny toy graphs directly in the notebook:

```text
chain graph
star graph
ring graph
complete graph
two-community graph
small directed approval loop
small bipartite employee-topic graph
```

### Implementation tasks

Create functions:

```python
def describe_graph(G):
    ...

def plot_graph(G, title: str):
    ...
```

For each graph shape, compute:

```text
number of nodes
number of edges
density
degree distribution
connected components
average clustering where applicable
```

### Student exercises

1. Create a graph where one manager approves all requests.
2. Create a graph where work loops between Legal and Sales.
3. Create a graph where one document references many policies.
4. Explain how each graph shape could create operational risk.

### Proper solution should show

- Visualizations of each graph shape.
- A table comparing metrics across graph shapes.
- Clear explanation that graph shape affects algorithm behavior.

---

## Lesson 02 — NetworkX foundations

### Goal

Teach practical graph construction in Python.

### Primary graph concepts

```text
Graph
DiGraph
MultiGraph
node attributes
edge attributes
edge lists
adjacency lists
subgraphs
filtering
import/export
```

### Corporate example context

Use a small support-ticket dataset.

### Dataset generation

Create a small synthetic support dataset:

```text
20 customers
50 tickets
10 agents
5 products
8 issue types
```

### Graph model

```text
Customer -> CREATED -> Ticket
Ticket -> ABOUT -> Issue
Ticket -> AFFECTS -> Product
Ticket -> ASSIGNED_TO -> Agent
Ticket -> RESOLVED_BY -> Agent
```

In NetworkX, represent this first as a heterogeneous directed graph. Use node attributes:

```text
node_type
name
team
product_area
```

Use edge attributes:

```text
relationship_type
timestamp
weight
cost
```

### Implementation tasks

Create helper functions:

```python
def add_typed_node(G, node_id, node_type, **attrs):
    ...

def add_typed_edge(G, src, dst, rel_type, **attrs):
    ...

def filter_nodes_by_type(G, node_type):
    ...

def filter_edges_by_type(G, rel_type):
    ...
```

### Student exercises

1. Add a new node type `KnowledgeArticle`.
2. Connect tickets to articles with `REFERENCED` edges.
3. Create a subgraph of only tickets, agents, and issues.
4. Export the graph to GraphML.

### Proper solution should show

- How to construct graphs from tables.
- How to work with attributes.
- How to filter graph elements.
- How to build a business graph without Neo4j yet.

---

## Lesson 03 — Graph profiling and basic metrics

### Goal

Teach how to inspect a graph before applying advanced algorithms.

### Primary graph concepts

```text
node count
edge count
density
degree distribution
in-degree
out-degree
connected components
weakly connected components
strongly connected components
isolates
bridges
clustering coefficient
assortativity
```

### Corporate example context

Use a document-policy graph.

### Dataset generation

Generate:

```text
100 documents
15 policy topics
10 owners
8 teams
300 references
200 usage events
```

Inject:

```text
one obsolete document with high usage
one ownerless critical document
one isolated document cluster
one dense duplicate-document cluster
```

### Graph model

```text
Document -> REFERENCES -> Document
Document -> ABOUT -> Topic
Document -> OWNED_BY -> Person
Team -> USES -> Document
Document -> SUPERSEDES -> Document
```

### Implementation tasks

Create a graph profile report:

```python
def graph_profile(G):
    return {
        "nodes": ...,
        "edges": ...,
        "density": ...,
        "components": ...,
        "isolates": ...,
        "top_degree_nodes": ...,
        "avg_clustering": ...,
    }
```

Create charts:

```text
degree histogram
component size distribution
top node degree table
node type counts
edge type counts
```

### Student exercises

1. Find isolated documents.
2. Find dense document clusters.
3. Find documents without owners.
4. Find heavily used obsolete documents.
5. Explain why graph profiling should come before graph algorithms.

### Proper solution should show

- Graph profile table.
- Distribution plots.
- Interpreted anomalies.
- A short value-discovery note: bad document structure leads to search cost, compliance risk, and rework.

---

# Part II — Core Graph Algorithms

---

## Lesson 04 — Centrality algorithms

### Goal

Teach different meanings of importance in a graph.

### Primary graph concepts

```text
degree centrality
in-degree and out-degree
betweenness centrality
closeness centrality
harmonic centrality
PageRank
eigenvector centrality
broker nodes
bottleneck nodes
authority nodes
```

### Corporate example context

Use a hidden-expert and support-escalation graph.

### Dataset generation

Generate:

```text
80 employees
20 teams
60 topics
2,000 questions
1,500 answers
300 documents
1,000 tickets
```

Inject:

```text
one legacy billing expert answering 60% of billing questions
one integration engineer resolving 45% of escalations
one team acting as bridge between Sales, Finance, and Legal
one document that is referenced by many important documents
```

### Graph models

Create three graph projections:

#### Employee-question-topic graph

```text
Employee -> ANSWERED -> Question
Question -> ABOUT -> Topic
Employee -> MEMBER_OF -> Team
```

#### Employee collaboration graph

```text
Employee -> HELPED -> Employee
```

Weighted by number of question-answer interactions.

#### Document authority graph

```text
Document -> REFERENCES -> Document
```

### Implementation tasks

Compute:

```python
nx.degree_centrality(G)
nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.pagerank(G)
nx.eigenvector_centrality(G)
```

Create a comparison table:

```text
node_id
node_type
name
degree_rank
betweenness_rank
pagerank_rank
business_interpretation
```

### Required interpretation

Explain the difference:

```text
Degree centrality = many direct connections.
Betweenness centrality = lies on many paths, often a broker or bottleneck.
Closeness centrality = can reach others quickly.
PageRank = important because connected to important nodes.
Eigenvector centrality = influence through influential neighbors.
```

### Student exercises

1. Find the most overloaded expert.
2. Find the best cross-team broker.
3. Find the most authoritative document.
4. Compare degree vs PageRank rankings.
5. Explain why the top-degree node is not always the most strategically important node.

### Proper solution should show

- Centrality comparison table.
- Rank disagreement analysis.
- Identification of hidden experts and bottlenecks.
- Explanation of what each centrality means in corporate terms.

---

## Lesson 05 — Community detection

### Goal

Teach how to find natural groups, clusters, silos, and issue families in graphs.

### Primary graph concepts

```text
community
cluster
modularity
label propagation
Louvain method
Leiden method if available
connected components vs communities
triangle count
local clustering coefficient
```

### Corporate example context

Use support tickets and customer feedback clusters.

### Dataset generation

Generate:

```text
2,000 tickets
100 customers
25 products/modules
50 issue labels
40 agents
100 knowledge articles
```

Inject:

```text
three issue families that are not obvious from labels alone
one product module that appears across multiple issue communities
one siloed support team that handles only a narrow cluster
one issue community with high escalation cost
```

### Graph projections

Create:

#### Ticket similarity graph

Connect tickets if they share:

```text
same issue type
same product
same knowledge article
same resolver
similar text category
```

#### Issue-product bipartite projection

```text
Issue <-> Product
```

#### Agent-issue projection

```text
Agent <-> Issue
```

### Implementation tasks

Use NetworkX algorithms:

```python
from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community import label_propagation_communities
```

If `python-louvain` is installed, also use Louvain.

Create outputs:

```text
community_id
community_size
top_issue_types
top_products
avg_escalation_rate
avg_resolution_time
estimated_cost
```

### Student exercises

1. Detect ticket communities.
2. Rank communities by support cost.
3. Identify product modules that bridge multiple communities.
4. Compare label propagation vs modularity-based communities.
5. Explain how communities differ from simple category labels.

### Proper solution should show

- Community assignment table.
- Community summary table.
- Visualization of ticket communities.
- Business interpretation of at least three communities.

---

## Lesson 06 — Paths, cycles, and dependencies

### Goal

Teach path-based reasoning: shortest paths, dependency chains, critical paths, cycles, and rework loops.

### Primary graph concepts

```text
path
shortest path
weighted shortest path
Dijkstra
A star conceptually
cycle
directed acyclic graph
strongly connected component
topological sort
critical path
impact analysis
```

### Corporate example context

Use approval chains and finance-reporting dependencies.

### Dataset generation

Generate two small datasets:

#### Approval event log

```text
1,000 requests
8 workflow states
50 actors
timestamps
request value
missing fields count
```

Inject:

```text
40% of Legal Review cases loop back to Requester because of missing fields
one approval path adds four days with little decision impact
high-value approvals have many unnecessary variants
```

#### Finance reporting dependency graph

```text
50 reports
100 spreadsheets
20 systems
80 metrics
30 owners
```

Inject:

```text
one board metric depends on a manual spreadsheet
one upstream table delays many reports
one circular spreadsheet dependency
three conflicting KPI definitions
```

### Implementation tasks

For approval graph:

```text
build directly-follows graph
weight edges by frequency
weight edges by average duration
find cycles
find most common paths
find slowest handoffs
```

For finance dependency graph:

```text
build directed dependency graph
find ancestors and descendants
find cycles
run topological sort if acyclic
find longest dependency chain
find central dependency nodes
```

### Student exercises

1. Find rework loops in approval process.
2. Find slowest handoffs.
3. Find shortest path from request submitted to approved.
4. Find all dependencies of EBITDA metric.
5. Find what reports are affected if one source system fails.

### Proper solution should show

- Directly-follows graph.
- Cycle report.
- Critical dependency report.
- Example path explanations.
- Clear distinction between shortest path, most frequent path, and slowest path.

---

## Lesson 07 — Similarity, duplicates, and bipartite graphs

### Goal

Teach two-mode graphs, projections, similarity scoring, and duplicate detection.

### Primary graph concepts

```text
bipartite graph
two-mode network
projection
Jaccard similarity
cosine similarity
common neighbors
Adamic-Adar
resource allocation
node similarity
entity resolution
recommendation
```

### Corporate example context

Use procurement supplier duplication and employee-topic expertise mapping.

### Dataset generation

Generate supplier data:

```text
500 suppliers
8 business units
40 categories
1,500 contracts
20,000 invoices
30 locations
```

Inject:

```text
same supplier under multiple names
business units buying similar services from different suppliers
single-source supplier risk for key products
supplier-location risk concentration
```

Generate employee-topic data:

```text
100 employees
80 topics
2,000 question-answer interactions
300 documents
```

Inject:

```text
one topic has high demand but only one expert
several employees have overlapping knowledge
one critical topic has no documentation
```

### Graph models

Supplier-category bipartite graph:

```text
Supplier <-> Category
Supplier <-> BusinessUnit
Supplier <-> Location
Supplier <-> Contract
```

Employee-topic bipartite graph:

```text
Employee <-> Topic
Employee <-> Document
Topic <-> Document
```

### Implementation tasks

Compute:

```text
bipartite projections
Jaccard similarity between suppliers
common-neighbor similarity
supplier duplicate candidates
employee expertise overlap
topic coverage risk
```

### Student exercises

1. Find duplicate supplier candidates.
2. Find supplier consolidation opportunities.
3. Find business units buying similar categories separately.
4. Find topics with one-person knowledge dependency.
5. Recommend backup experts for each critical topic.

### Proper solution should show

- Bipartite graph visual example.
- Supplier similarity table.
- Duplicate supplier candidate list.
- Expert-topic coverage table.
- Explanation of projection risks: projections can create dense graphs and inflate relationships.

---

## Lesson 08 — Temporal and process graphs

### Goal

Teach how graphs change over time and how event logs become process graphs.

### Primary graph concepts

```text
event log
case id
activity
resource
timestamp
directly-follows graph
process variant
temporal edge
time-window graph
evolving centrality
before/after comparison
queue time
cycle time
```

### Corporate example context

Use approval workflows, support escalation, and finance close.

### Dataset generation

Generate event logs:

```text
approval_events.csv
support_ticket_events.csv
finance_close_events.csv
```

Each event log must include:

```text
case_id
activity
actor
team
timestamp
cost_or_value
```

Inject:

```text
approval rework loop before intervention
support escalation spike in one month
finance close bottleneck in one recurring handoff
```

### Implementation tasks

Create directly-follows graph manually using Pandas:

```python
def build_directly_follows_edges(events, case_col, activity_col, timestamp_col):
    ...
```

Compute:

```text
edge frequency
average transition time
median transition time
p90 transition time
variant count
case duration
rework loop frequency
```

Optionally use PM4Py for:

```text
process discovery
DFG visualization
variant analysis
```

### Student exercises

1. Build a directly-follows graph from event logs.
2. Find the most common process variant.
3. Find the slowest transition.
4. Compare process graph before and after a simulated AI intake checker.
5. Explain why process mining complements graph analytics.

### Proper solution should show

- Directly-follows graph table.
- Process variant summary.
- Transition-time heatmap or table.
- Before/after graph comparison.
- Clear explanation of process graph vs entity relationship graph.

---

# Part III — Neo4j and Property Graphs

---

## Lesson 09 — Neo4j property graph modeling

### Goal

Teach property graph modeling and Cypher basics.

### Primary graph concepts

```text
labels
relationship types
node properties
relationship properties
constraints
indexes
MERGE
MATCH
OPTIONAL MATCH
paths
variable-length paths
```

### Corporate example context

Use a document-policy graph and support escalation graph.

### Implementation tasks

Create:

```text
cypher/00_constraints.cypher
cypher/01_load_support_escalation.cypher
cypher/04_load_document_policy.cypher
```

Create constraints such as:

```cypher
CREATE CONSTRAINT document_id IF NOT EXISTS
FOR (d:Document) REQUIRE d.document_id IS UNIQUE;

CREATE CONSTRAINT ticket_id IF NOT EXISTS
FOR (t:Ticket) REQUIRE t.ticket_id IS UNIQUE;
```

Create loading queries using `LOAD CSV WITH HEADERS` or Python driver batch loads.

### Graph models

Support graph:

```text
(:Customer)-[:CREATED]->(:Ticket)
(:Ticket)-[:ABOUT]->(:Issue)
(:Ticket)-[:AFFECTS]->(:Product)
(:Ticket)-[:ASSIGNED_TO]->(:Agent)
(:Ticket)-[:ESCALATED_TO]->(:Team)
(:Ticket)-[:RESOLVED_BY]->(:Agent)
(:Ticket)-[:REFERENCED]->(:KnowledgeArticle)
```

Document graph:

```text
(:Document)-[:REFERENCES]->(:Document)
(:Document)-[:SUPERSEDES]->(:Document)
(:Document)-[:OWNED_BY]->(:Person)
(:Team)-[:USES]->(:Document)
(:Document)-[:ABOUT]->(:Topic)
```

### Student exercises

1. Load support graph into Neo4j.
2. Count nodes by label.
3. Count relationships by type.
4. Find tickets escalated to Engineering.
5. Find documents that reference obsolete documents.
6. Find documents with no owner.

### Proper solution should show

- Neo4j connection setup.
- Constraints and indexes.
- Data loading.
- Basic Cypher queries.
- Explanation of why property graphs are useful for exploration.

---

## Lesson 10 — Cypher path queries

### Goal

Teach graph query thinking using Cypher paths.

### Primary graph concepts

```text
pattern matching
path matching
variable-length traversal
shortest path concept
subgraph extraction
anti-pattern queries
existence checks
impact analysis
```

### Corporate example context

Use finance reporting dependencies, compliance controls, and document policies.

### Dataset generation

Use previously generated datasets:

```text
finance_reporting
compliance_controls
document_policy
```

### Required Cypher query examples

Find ownerless critical documents:

```cypher
MATCH (d:Document)
WHERE d.criticality = 'high'
  AND NOT (d)-[:OWNED_BY]->(:Person)
RETURN d.document_id, d.title, d.criticality;
```

Trace report lineage:

```cypher
MATCH path = (r:Report {name: $report_name})-[:DEPENDS_ON|PULLS_FROM|CALCULATED_FROM*1..6]->(source)
RETURN path;
```

Find policy impact:

```cypher
MATCH path = (p:Policy {policy_id: $policy_id})<-[:SATISFIED_BY|REFERENCES|EVIDENCED_BY*1..5]-(affected)
RETURN path;
```

Find unresolved support issue chains:

```cypher
MATCH path = (c:Customer)-[:CREATED]->(t:Ticket)-[:AFFECTS]->(p:Product)
WHERE t.status <> 'resolved'
RETURN path
LIMIT 50;
```

### Student exercises

1. Write a query that finds all downstream reports affected by a broken source system.
2. Write a query that finds controls without evidence.
3. Write a query that finds obsolete documents still used by teams.
4. Write a query that finds all support tickets touching a high-risk product.
5. Write a query that returns an evidence path from regulation to control to policy to evidence document.

### Proper solution should show

- Query library with business explanations.
- At least 20 reusable Cypher queries.
- Example outputs in notebooks.
- No hard-coded IDs unless clearly marked as examples.

---

## Lesson 11 — Neo4j Graph Data Science workflow

### Goal

Teach the Neo4j GDS operating model.

### Primary graph concepts

```text
graph projection
named in-memory graph
graph catalog
memory estimation
algorithm execution modes
stream mode
stats mode
mutate mode
write mode
node properties
relationship properties
cleanup/drop graph
```

### Corporate example context

Use document authority, support escalation, and hidden expert graphs.

### Implementation tasks

Create a notebook that demonstrates the GDS lifecycle:

```text
1. Connect to Neo4j.
2. Verify GDS is installed.
3. Create projection.
4. Estimate memory.
5. Run algorithm in stream mode.
6. Run algorithm in mutate mode.
7. Run algorithm in write mode.
8. Query results with Cypher.
9. Drop named graph.
```

### Required GDS examples

PageRank on document references:

```cypher
CALL gds.graph.project(
  'document_reference_graph',
  'Document',
  'REFERENCES'
);

CALL gds.pageRank.stream('document_reference_graph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).title AS document, score
ORDER BY score DESC
LIMIT 20;
```

Weakly connected components on supplier graph:

```cypher
CALL gds.wcc.stream('supplier_graph')
YIELD nodeId, componentId
RETURN componentId, count(*) AS size
ORDER BY size DESC;
```

Louvain on ticket similarity graph if projected:

```cypher
CALL gds.louvain.stream('ticket_similarity_graph')
YIELD nodeId, communityId
RETURN communityId, count(*) AS size
ORDER BY size DESC;
```

### Student exercises

1. Project a graph for document references.
2. Run PageRank.
3. Write PageRank score back to Neo4j.
4. Query top PageRank documents using Cypher.
5. Drop the graph projection.
6. Repeat with a support or supplier graph.

### Proper solution should show

- GDS workflow diagram.
- Explanation of stream/mutate/write/stats.
- Memory estimation example.
- Cleanup step.
- Comparison of NetworkX vs Neo4j GDS results on a small graph.

---

# Part IV — Graph Data Science and Machine Learning

---

## Lesson 12 — Graph features for machine learning

### Goal

Teach how graph metrics become ML features.

### Primary graph concepts

```text
feature engineering
node-level features
edge-level features
graph-level features
centrality features
community features
degree features
triangle features
train/test split
baseline model
feature importance
```

### Corporate example context

Predict support escalation risk or project margin leakage.

### Dataset generation

Use support escalation dataset and project margin dataset.

For support escalation, generate labels:

```text
ticket_escalated = 0/1
resolution_time_hours
support_cost
```

For project margin, generate labels:

```text
low_margin_project = 0/1
margin_percent
late_delivery = 0/1
```

Inject patterns:

```text
tickets in certain issue communities have higher escalation probability
projects with dependency cycles and expert escalations have lower margin
```

### Implementation tasks

Create features:

```text
degree centrality
PageRank
community id
number of triangles
neighbor escalation rate
product support burden
agent workload centrality
path distance to engineering team
```

Train simple models:

```text
LogisticRegression
RandomForestClassifier
```

Compare:

```text
baseline tabular features only
graph features only
tabular + graph features
```

### Student exercises

1. Build graph features for tickets.
2. Train escalation prediction model.
3. Compare model with and without graph features.
4. Interpret which graph features matter.
5. Explain why the model should support process improvement, not replace management judgment.

### Proper solution should show

- Feature table.
- Model comparison table.
- Feature importance chart.
- Clear warning about synthetic data and responsible interpretation.

---

## Lesson 13 — Embeddings and link prediction

### Goal

Teach how graph structure can be represented as vectors and used to predict missing relationships.

### Primary graph concepts

```text
node embedding
structural similarity
neighborhood similarity
Node2Vec concept
FastRP concept
link prediction
common neighbors
Adamic-Adar
preferential attachment
resource allocation
negative sampling
recommendation
```

### Corporate example context

Use document recommendation, supplier similarity, and cross-sell opportunity discovery.

### Dataset generation

Use three datasets:

```text
document_policy
supplier_risk
sales_accounts
```

Inject:

```text
missing document-policy links
supplier duplicate candidates
cross-sell products that similar accounts already use
```

### Implementation tasks

Python-only link prediction:

```python
nx.common_neighbors(G, u, v)
nx.adamic_adar_index(G)
nx.preferential_attachment(G)
nx.resource_allocation_index(G)
```

If possible, include optional embedding approach:

```text
node2vec package if available
or simple matrix-factorization style demonstration
or Neo4j GDS FastRP/Node2Vec if GDS supports it locally
```

### Student exercises

1. Predict missing document-topic links.
2. Recommend knowledge articles for tickets.
3. Recommend cross-sell products to accounts.
4. Compare common-neighbor and embedding-based recommendations.
5. Explain when link prediction is useful and when it is risky.

### Proper solution should show

- Candidate missing links ranked by score.
- Explanation columns for each recommendation.
- Precision check against synthetic ground truth.
- Human review requirement for business use.

---

## Lesson 14 — Optional GraphRAG evidence graph

### Goal

Show how graph structure can support retrieval and evidence navigation for AI assistants.

### Primary graph concepts

```text
knowledge graph
evidence graph
claim-evidence relationship
entity extraction concept
graph traversal for context
source provenance
graph + vector retrieval concept
```

### Corporate example context

Use compliance controls or medical-style document evidence, but keep it simple.

### Dataset generation

Generate:

```text
50 policies
200 evidence documents
100 controls
30 regulations
300 claims
500 evidence items
```

Inject:

```text
some claims unsupported
some controls missing evidence
some evidence documents obsolete
some regulations linked to many downstream policies
```

### Graph model

```text
(:Regulation)-[:REQUIRES]->(:Control)
(:Control)-[:SATISFIED_BY]->(:Policy)
(:Claim)-[:SUPPORTED_BY]->(:EvidenceItem)
(:EvidenceItem)-[:FROM_DOCUMENT]->(:Document)
(:EvidenceItem)-[:FROM_PAGE]->(:Page)
(:Policy)-[:REFERENCES]->(:Policy)
```

### Implementation tasks

Create simple graph retrieval functions:

```python
def retrieve_evidence_for_claim(claim_id):
    ...

def find_unsupported_claims():
    ...

def trace_regulation_to_evidence(regulation_id):
    ...
```

Do not build a full LLM application. The goal is graph retrieval, not chatbot UI.

### Student exercises

1. Find unsupported claims.
2. Trace one regulation to evidence documents.
3. Find obsolete evidence still supporting active controls.
4. Build a prompt context block from graph evidence.
5. Explain how graph retrieval reduces hallucination risk.

### Proper solution should show

- Evidence path outputs.
- Citation/provenance fields.
- Unsupported claim report.
- A minimal prompt context example.

---

# Part V — Capstone Corporate Graph Exercises

The following capstones are larger exercises that combine several graph techniques. They should be implemented after the foundational lessons.

Each capstone must follow this structure:

```text
1. Business context
2. Graph learning goals
3. Synthetic data generation
4. Graph schema
5. Required algorithms
6. Notebook tasks
7. Expected findings
8. Value discovery note
9. Proper solution checklist
10. Optional extension
```

---

## Capstone 15 — Support escalation graph

### Business context

A PE-backed SaaS company has rising support costs and slow escalations. Management wants to understand whether the real issue is product quality, support routing, missing knowledge articles, or overdependence on senior engineers.

### Graph learning goals

Teach:

```text
heterogeneous graph modeling
centrality
community detection
similarity
bipartite issue-product analysis
path analysis
cost-weighted interpretation
```

### Synthetic data

Generate:

```text
customers.csv
agents.csv
teams.csv
products.csv
issues.csv
tickets.csv
ticket_events.csv
knowledge_articles.csv
ticket_article_usage.csv
```

Recommended size:

```text
300 customers
2,000 tickets
40 agents
8 teams
10 products
50 issue types
100 knowledge articles
8,000 ticket events
```

Injected ground truth:

```text
Billing API issues escalate 75% of the time.
One integration engineer resolves 45% of escalations.
Certain agents resolve similar cases faster due to hidden workarounds.
High-value customers are clustered around unresolved product issues.
Knowledge articles are missing for two high-volume issue communities.
```

### Required algorithms

```text
degree centrality
betweenness centrality
PageRank optional
community detection
node similarity
bipartite projection
path frequency
```

### Notebook tasks

1. Build graph from tables.
2. Profile graph.
3. Find escalation-heavy issue/product pairs.
4. Find overloaded experts.
5. Detect ticket communities.
6. Find knowledge article gaps.
7. Estimate cost of top escalation clusters.
8. Propose graph-informed AI intervention points.

### Proper solution checklist

The final notebook should produce:

```text
Top 10 issue/product escalation hotspots
Top 10 expert dependency nodes
Issue communities ranked by cost
Knowledge article gap list
Customer risk cluster list
One-page markdown summary
```

### Value discovery note

Use findings to motivate:

```text
AI ticket triage
AI resolution recommender
AI escalation packet generator
AI knowledge article generator
AI churn-risk summarizer
```

---

## Capstone 16 — Approval and handoff graph

### Business context

A company has slow procurement and contract approvals. Teams disagree about where delays happen.

### Graph learning goals

Teach:

```text
event-log to process graph
directly-follows graph
cycle detection
variant analysis
queue-time analysis
edge weighting
bottleneck interpretation
```

### Synthetic data

Generate:

```text
requests.csv
approval_events.csv
actors.csv
teams.csv
policies.csv
```

Recommended size:

```text
1,000 requests
8,000 events
60 actors
8 workflow states
5 request types
```

Injected ground truth:

```text
40% of legal reviews loop back due to missing information.
High-value approvals follow 12 variants instead of 3 standard paths.
One approval step adds four days but rarely changes decisions.
One business unit repeatedly submits incomplete requests.
```

### Required algorithms

```text
directly-follows graph
cycle detection
path frequency
weighted edge analysis
betweenness centrality on states
variant analysis
```

### Notebook tasks

1. Build event log.
2. Build directly-follows graph.
3. Compute edge frequencies and transition durations.
4. Detect rework loops.
5. Rank slowest handoffs.
6. Identify process variants.
7. Simulate removal of one low-value approval step.
8. Summarize AI intake checker opportunity.

### Proper solution checklist

The final notebook should produce:

```text
Directly-follows graph
Top 10 process variants
Top rework loops
Transition-time table
Approval-step impact table
Recommended simplified process paths
```

### Value discovery note

Use findings to motivate:

```text
AI intake checker
AI missing-information detector
AI approval summary generator
AI routing workflow
AI policy pre-checker
```

---

## Capstone 17 — Hidden experts and tribal knowledge graph

### Business context

A legacy business depends on a few experts. Work slows when they are busy or unavailable.

### Graph learning goals

Teach:

```text
expertise graph construction
bipartite employee-topic graph
centrality
coverage analysis
community detection
knowledge gap identification
```

### Synthetic data

Generate:

```text
employees.csv
teams.csv
topics.csv
systems.csv
questions.csv
answers.csv
documents.csv
tickets.csv
```

Recommended size:

```text
100 employees
80 topics
20 systems
3,000 questions
3,000 answers
400 documents
2,000 tickets
```

Injected ground truth:

```text
One legacy billing expert answers 60% of billing questions.
Critical system has very little documentation.
New employees repeatedly ask the same people.
Old tickets contain better answers than official SOPs.
```

### Required algorithms

```text
degree centrality
betweenness centrality
PageRank optional
bipartite projection
topic coverage scoring
community detection
```

### Notebook tasks

1. Build employee-topic-system graph.
2. Rank experts by topic.
3. Detect single-person dependency topics.
4. Find topics with high question volume and low documentation.
5. Recommend backup experts.
6. Generate SOP extraction backlog.

### Proper solution checklist

The final notebook should produce:

```text
Expert ranking by topic
Critical topic coverage table
Documentation gap report
Single-person dependency risk list
Suggested SOP creation backlog
```

### Value discovery note

Use findings to motivate:

```text
RAG knowledge assistant
expert locator
AI-generated SOP drafts
ticket-to-knowledge-base agent
knowledge freshness monitor
```

---

## Capstone 18 — Supplier risk and procurement graph

### Business context

A PE-backed company has fragmented vendor data and possible procurement savings.

### Graph learning goals

Teach:

```text
supplier-category graph
entity resolution
similarity
dependency centrality
risk propagation
single-source risk
spend-weighted graph interpretation
```

### Synthetic data

Generate:

```text
suppliers.csv
business_units.csv
categories.csv
contracts.csv
invoices.csv
locations.csv
products.csv
risk_events.csv
```

Recommended size:

```text
500 suppliers
8 business units
40 categories
1,500 contracts
20,000 invoices
50 products
30 locations
100 risk events
```

Injected ground truth:

```text
Same vendor appears under multiple names.
Three business units buy similar services separately.
One supplier is critical for several high-revenue products.
One risky location affects several suppliers.
```

### Required algorithms

```text
Jaccard similarity
connected components
community detection
centrality
risk propagation
path analysis
```

### Notebook tasks

1. Build supplier graph.
2. Detect duplicate supplier candidates.
3. Find spend fragmentation by category.
4. Rank suppliers by dependency centrality.
5. Simulate supplier failure.
6. Estimate revenue at risk.
7. Build procurement opportunity table.

### Proper solution checklist

The final notebook should produce:

```text
Duplicate supplier clusters
Consolidation opportunity list
Single-source risk ranking
Revenue-at-risk report
Supplier-location risk map
```

### Value discovery note

Use findings to motivate:

```text
AI supplier consolidation assistant
contract-risk summarizer
supplier-risk monitor
procurement negotiation prep assistant
spend classification agent
```

---

## Capstone 19 — Portfolio-company benchmark graph

### Business context

A PE operating team wants to compare companies and identify repeatable AI value-creation patterns.

### Graph learning goals

Teach:

```text
meta-graph modeling
company similarity
pattern mining
community detection
link prediction
benchmarking
playbook graph construction
```

### Synthetic data

Generate:

```text
portfolio_companies.csv
processes.csv
pain_points.csv
systems.csv
ai_interventions.csv
value_levers.csv
metrics.csv
use_cases.csv
```

Recommended size:

```text
12 portfolio companies
200 processes
500 pain points
300 systems
150 AI interventions
80 value levers
```

Injected ground truth:

```text
Support escalation problems repeat across SaaS companies.
Procurement fragmentation repeats across manufacturing companies.
Finance close bottlenecks repeat across services companies.
Poor documentation correlates with longer onboarding.
```

### Required algorithms

```text
similarity
community detection
centrality
link prediction
pattern frequency
benchmark scoring
```

### Notebook tasks

1. Build portfolio operating graph.
2. Cluster companies by operational similarity.
3. Find repeated pain-point communities.
4. Recommend AI interventions based on similar companies.
5. Rank value levers by recurrence and estimated impact.
6. Generate a portfolio value-creation heatmap.

### Proper solution checklist

The final notebook should produce:

```text
Company similarity map
Repeated pain-point clusters
AI intervention recommendation table
Portfolio value-creation heatmap
Reusable PE playbook graph
```

### Value discovery note

Use findings to motivate:

```text
AI use-case recommender
portfolio benchmarking assistant
value-creation playbook generator
operating partner copilot
```

---

# Part VI — Documentation files to generate

---

## docs/graph_algorithm_cheatsheet.md

Create a concise cheat sheet with:

```text
Algorithm
Question it answers
Input graph type
Output
Corporate example
Common mistake
```

Include:

```text
degree centrality
betweenness centrality
closeness centrality
PageRank
connected components
strongly connected components
label propagation
Louvain
shortest path
Dijkstra
cycle detection
topological sort
Jaccard similarity
common neighbors
Adamic-Adar
resource allocation
node embeddings
link prediction
```

---

## docs/graph_modeling_patterns.md

Create reusable graph modeling patterns:

```text
Person-task graph
Ticket-escalation graph
Document-policy graph
Approval-process graph
Supplier-category graph
System-dependency graph
Metric-lineage graph
Customer-product-feedback graph
Compliance-control-evidence graph
Portfolio-company-operating graph
```

For each pattern include:

```text
nodes
relationships
important properties
questions answered
useful algorithms
pitfalls
```

---

## docs/networkx_quick_reference.md

Include practical examples for:

```text
creating graphs
adding attributes
loading edge lists
filtering nodes
subgraphs
centrality
communities
shortest paths
components
similarity
visualization
export
```

---

## docs/neo4j_quick_reference.md

Include:

```text
Neo4j connection setup
constraints
indexes
LOAD CSV
MERGE patterns
MATCH patterns
path queries
variable-length paths
aggregation
cleaning database
GDS projection basics
GDS execution modes
```

---

## docs/process_graphs_quick_reference.md

Include:

```text
event log structure
case id
activity
timestamp
resource
directly-follows graph
variant analysis
transition-time analysis
cycle/rework detection
before/after comparison
```

---

## docs/pe_corporate_use_case_map.md

Create a business-context map, but keep it secondary.

Include:

```text
Use case
Graph model
Algorithms
Possible AI intervention
Value lever
Learning lesson where it appears
```

Use cases:

```text
support escalation
approval handoffs
hidden experts
document policy
supplier risk
finance reporting
project margin leakage
IT incidents
compliance controls
sales account relationships
product feedback
portfolio benchmark
```

---

# Part VII — Testing requirements

---

## Data-generation tests

Create tests that verify:

```text
all generated files exist
required columns exist
foreign keys are valid
row counts are within expected range
no null IDs
random seed makes data deterministic
injected ground-truth entities exist
```

Example:

```python
def test_support_escalation_ground_truth_exists():
    ground_truth = load_json("data/generated/support_escalation/ground_truth.json")
    assert len(ground_truth["injected_patterns"]) >= 3
```

---

## Graph-builder tests

Verify:

```text
graph has expected node count
edge types are present
node types are present
no orphan IDs from relationship tables
critical injected nodes appear in graph
```

---

## Metric tests

Use tiny known graphs to test:

```text
degree centrality
connected components
cycle detection
shortest paths
bipartite projection
```

---

# Part VIII — Learning quality bar

A lesson is complete only if a student can answer:

```text
1. What graph concept did I learn?
2. What graph did I build?
3. What algorithm did I run?
4. What does the algorithm output mean?
5. What can go wrong when interpreting it?
6. How does the corporate example illustrate the graph concept?
7. What would be the next AI/value intervention after the graph finding?
```

The notebook should not merely compute. It should teach interpretation.

---

# Part IX — Suggested learning sequence

Use this order for self-study:

```text
Day 01: Environment check and graph shapes
Day 02: NetworkX foundations
Day 03: Graph profiling
Day 04: Centrality
Day 05: Community detection
Day 06: Paths, cycles, and dependencies
Day 07: Similarity and bipartite graphs
Day 08: Temporal and process graphs
Day 09: Neo4j modeling
Day 10: Cypher path queries
Day 11: Neo4j GDS workflow
Day 12: Graph features for ML
Day 13: Embeddings and link prediction
Day 14: Optional GraphRAG evidence graph
Day 15–19: Capstone notebooks
```

Recommended cadence:

```text
1 lesson per day for intensive study
2 lessons per week for part-time study
capstones as weekend projects
```

---

# Part X — Final acceptance criteria for the whole repo

The generated repo is successful when:

```text
1. `make install` works.
2. `make generate-data` creates all synthetic datasets.
3. `make test` passes.
4. `notebooks/00_environment_check.ipynb` runs.
5. Lessons 01–08 run without Neo4j.
6. Neo4j lessons fail gracefully if Neo4j is unavailable.
7. At least one Cypher loading script works against local Neo4j.
8. At least one GDS algorithm runs if GDS is available.
9. Every lesson includes exercises and interpretation.
10. Every capstone includes a proper solution checklist.
11. The repo remains notebook-first and does not include unnecessary UI.
12. The PE/corporate context supports the graph learning, but does not dominate it.
```

---

# Part XI — AI agent implementation order

The coding AI agent should implement the repo in this order:

```text
1. Create repo skeleton.
2. Create requirements.txt, pyproject.toml, Makefile, README.md.
3. Implement common utilities.
4. Implement support escalation data generation first.
5. Implement graph builder utilities.
6. Implement Lesson 00.
7. Implement Lessons 01–04.
8. Add tests for generated data and graph builders.
9. Implement Lessons 05–08.
10. Add Neo4j Docker Compose and connection helpers.
11. Implement Lessons 09–11.
12. Implement ML Lessons 12–13.
13. Implement optional GraphRAG Lesson 14.
14. Implement capstones 15–19.
15. Generate docs cheat sheets.
16. Run `make verify`.
17. Fix failures.
18. Produce final README usage instructions.
```

Do not attempt to build everything in one huge untested change. Build in small increments.

---

# Part XII — README requirements

The README must include:

```text
1. What this repo teaches.
2. What is intentionally not included.
3. Setup instructions.
4. Python-only mode instructions.
5. Neo4j mode instructions.
6. How to generate data.
7. How to run notebooks.
8. Recommended lesson order.
9. Troubleshooting.
10. How to extend with new corporate graph use cases.
```

Include this positioning statement:

> This masterclass teaches graph thinking, graph analytics, and graph data science. Private-equity and corporate value discovery scenarios are used as practical examples because real companies are full of relationships, dependencies, handoffs, bottlenecks, and hidden networks.

---

# Part XIII — Final note on philosophy

The core learning loop of the masterclass is:

```text
model the relationship
→ build the graph
→ inspect the structure
→ run the algorithm
→ interpret the result
→ connect the finding to a real workflow problem
→ only then discuss AI intervention
```

The student should finish the masterclass understanding that graph data science is not just about running algorithms. It is about seeing structure that tables, process diagrams, and dashboards often hide.
