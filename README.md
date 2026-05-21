# Graph Masterclass — Learning Repository

**Teaching graph thinking, analytics, and algorithms through runnable local notebooks.**

## Overview

A comprehensive learning environment for graph analysis with:
- 19 progressive lessons covering graph foundations to advanced techniques
- Synthetic corporate datasets for realistic problem-solving
- NetworkX-based Python analytics
- Neo4j and Cypher examples (optional, for advanced lessons)
- Capstone projects with real business scenarios

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (for Neo4j, optional)

### Installation

```bash
# Clone or navigate to the repo
cd pe-graph-value-masterclass

# Install dependencies
make install

# Verify environment
jupyter lab notebooks/00_environment_check.ipynb
```

### Two Learning Modes

**Mode A — Python-only** (Lessons 0-8, 12-13)
```bash
make jupyter
# No Neo4j required
```

**Mode B — Neo4j** (Lessons 9-11, 14)
```bash
make neo4j-up
make neo4j-load-data
make jupyter
```

## Course Structure

### Part I — Graph Foundations (Lessons 0-3)
- Lesson 00: Environment check
- Lesson 01: Graph thinking and shapes
- Lesson 02: NetworkX foundations
- Lesson 03: Graph profiling and metrics

### Part II — Core Algorithms (Lessons 4-8)
- Lesson 04: Centrality algorithms
- Lesson 05: Community detection
- Lesson 06: Paths, cycles, dependencies
- Lesson 07: Bipartite graphs
- Lesson 08: Temporal and process graphs

### Part III — Neo4j & Graph Data Science (Lessons 9-13)
- Lesson 09: Property graph modeling
- Lesson 10: Cypher path queries
- Lesson 11: Neo4j GDS workflow
- Lesson 12: Graph features for ML
- Lesson 13: Embeddings and link prediction

### Part IV — Advanced & Capstone (Lessons 14-19)
- Lesson 14: GraphRAG evidence graphs (optional)
- Lessons 15-19: Capstone projects on real business scenarios

## Key Commands

```makefile
make install              # Install dependencies
make lint                 # Run linter
make format              # Format code
make test                # Run tests
make jupyter             # Start JupyterLab
make generate-data       # Generate all synthetic datasets
make neo4j-up            # Start Neo4j container
make neo4j-down          # Stop Neo4j container
make verify              # Lint + test
```

## Technology Stack

### Core Libraries
- **pandas**, **numpy** — Data manipulation
- **networkx** — Python graph library
- **matplotlib**, **pyvis** — Visualization
- **scikit-learn** — Machine learning
- **duckdb** — Lightweight analytics
- **faker** — Synthetic data generation
- **neo4j** — Graph database driver
- **graphdatascience** — Neo4j GDS client

### Development
- **pytest** — Testing framework
- **ruff** — Fast linting and formatting
- **jupyter** — Interactive notebooks

## Learning Objectives

By completing this masterclass, you will understand:

- ✓ Graph shapes and why structure matters
- ✓ How to construct graphs from relational data
- ✓ Core metrics: density, centrality, clustering
- ✓ Algorithms: PageRank, community detection, shortest paths
- ✓ Graph-based machine learning and embeddings
- ✓ Real-world applications in corporate analytics
- ✓ How to model complex domains as graphs
- ✓ When graphs are better than tables

## File Structure

```
pe-graph-value-masterclass/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project metadata
├── docker-compose.yml        # Neo4j service definition
├── Makefile                  # Build and run commands
├── .env.example              # Environment template
│
├── notebooks/                # All 19 lesson notebooks
├── data/                     # Datasets
│   ├── seed/                 # Static seed data
│   ├── generated/            # Generated synthetic data
│   └── processed/            # Output and processed data
├── src/                      # Python modules
│   ├── data_generation/      # Synthetic data generators
│   ├── graph_builders/       # Graph construction
│   ├── analytics/            # Graph algorithms
│   ├── reporting/            # Output and visualization
│   ├── utils/                # Shared utilities
│   └── config.py             # Configuration
├── cypher/                   # Cypher query scripts
├── reports/                  # Generated reports and templates
└── tests/                    # Unit tests
```

## Self-Study Tips

1. **Complete Lesson 00 first** — Verifies your environment works
2. **Follow the numbered sequence** — Each lesson builds on prior concepts
3. **Run exercises and challenges** — Don't skip hands-on work
4. **Read value-discovery notes** — Understand business implications
5. **Experiment** — Modify the notebooks, try different parameters
6. **Take notes** — Graph thinking is a new mindset; consolidate your learning

## Neo4j Setup

Optional: If you want to use Neo4j:

```bash
# Start the service
make neo4j-up

# Load synthetic data into Neo4j
# (Run notebook 09 or use Cypher scripts in cypher/)

# Access Neo4j Browser
# Visit: http://localhost:7474

# Stop the service
make neo4j-down
```

Default credentials (change in .env):
- Username: `neo4j`
- Password: `your_password_here`

## Troubleshooting

### ImportError for networkx, pandas, etc.
```bash
make install
```

### Neo4j connection refused
```bash
make neo4j-up
# Wait 10 seconds for the container to start
```

### Jupyter kernel won't start
```bash
python -m ipykernel install --user
jupyter lab
```

## Contributing

This is a learning repository. If you find errors or have improvements:
- Check CONTRIBUTING.md (when available)
- Report issues clearly with notebook number and error message

## License

[Add license information here if applicable]

## Author Notes

This masterclass prioritizes:
- **Learning by doing** — Runnable code from day one
- **Clear progression** — Each lesson builds on the last
- **Realistic datasets** — Synthetic but representative of real-world problems
- **Intuitive explanations** — Graph thinking before math
- **Practical output** — Techniques applicable to real problems

Start with Lesson 00. Good luck!
