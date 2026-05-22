# Graph Data Science (GDS) Setup Guide

## Quick Start

The Docker configuration automatically installs the **Graph Data Science plugin** for Neo4j. No manual installation needed!

### First-Time Setup (Takes ~2-3 minutes)

```bash
cd /home/marek/Apps/graph-analysis-course
docker compose down    # Stop any existing containers
docker compose up -d   # Start with GDS plugin
```

**Wait for initialization**: The plugin downloads on first run (~60-90 seconds)

### Verify GDS is Working

Run this in **Lesson 11, Cell 6** (GDS Initialization):

```python
# If you see this output, GDS is ready:
✓ GDS client connected
✓ Graph Data Science version: 2.6.9
```

If you see this instead:
```
✗ GDS initialization failed
```
Then see troubleshooting section below.

---

## Why Do We Need GDS?

**Lesson 11** requires Graph Data Science for:
- PageRank algorithm (finding influential documents)
- Louvain community detection (finding document clusters)
- Centrality measures (identifying bottlenecks)
- 10-100x faster performance than NetworkX on large graphs

---

## System Requirements

| Component | Version | Status |
|-----------|---------|--------|
| Docker | 20.10+ | ✓ Required |
| Neo4j | 5.14 Community | ✓ Included |
| GDS Plugin | 2.6.9 | ✓ Auto-installed |
| Python | 3.11+ | ✓ Included in venv |
| graphdatascience client | 1.14+ | ✓ In requirements.txt |

---

## Troubleshooting

### Problem: "GDS not available - skipping..."

**Solution 1: Wait longer**
- First startup takes 2-3 minutes for plugin download
- Check logs: `docker compose logs neo4j | tail -20`
- Look for: `"GraphDataScience registered"`

**Solution 2: Restart containers**
```bash
docker compose down
docker compose up -d
# Wait 2 minutes, then test Lesson 11 Cell 6
```

**Solution 3: Clear and rebuild (nuclear option)**
```bash
# This deletes all data - only if stuck
docker compose down
docker volume rm neo4j-data
docker compose up -d
# Reload Lesson 09 (or seed with sample data)
```

### Problem: Container won't start

**Check Docker status:**
```bash
docker ps                    # See running containers
docker compose logs neo4j    # View detailed logs
```

**Port conflicts?**
```bash
# Neo4j needs ports 7474 (HTTP) and 7687 (Bolt)
netstat -tulpn | grep -E '7474|7687'
# If in use: Change in docker-compose.yml and restart
```

### Problem: Still seeing "GDS not available"?

**Check Python client:**
```bash
source venv/bin/activate
python -c "from graphdatascience import GraphDataScience; print('✓ GDS client installed')"
```

If error:
```bash
pip install graphdatascience==1.14.0
```

---

## Understanding the Setup

### docker-compose.yml Configuration

```yaml
environment:
  NEO4J_PLUGINS: '["graph-data-science"]'
```

This tells Neo4j to automatically download and install the GDS plugin on first startup.

### What Gets Downloaded

- **Plugin File**: ~250 MB
- **Location**: `/var/lib/neo4j/plugins/graph-data-science.jar`
- **License**: Community (unlicensed, but fully functional for education)

### Disk Space Required

- Neo4j database: 100-500 MB
- GDS plugin: 250 MB
- Data volumes: ~200 MB
- **Total: ~1 GB**

---

## Known Limitations

### GDS Procedures May Not Be Available in Community Edition
In some configurations, the GDS plugin registers successfully but GDS procedures like `gds.pagerank.stream` are not available. This is a Community Edition limitation that doesn't affect learning.

**What Works**:
- Graph projections: `gds.graph.project()` ✓
- GDS client initialization: `gds.version()` ✓
- Educational content and concepts ✓

**What May Not Work**:
- Algorithm execution: `gds.pagerank.stream()` ✗
- Algorithm mutations/writes ✗

**Workaround**: 
- Lesson 11 includes fallback output for all algorithms
- You can still understand algorithm concepts
- For production use: Deploy Neo4j Enterprise Edition

---

## Common Questions

**Q: Can I use GDS without Docker?**
A: Yes, but you'll need to:
1. Install Neo4j 5.14 desktop or server version
2. Manually download GDS plugin from neo4j.com (Enterprise or Community)
3. Add to Neo4j plugins directory
4. Restart Neo4j
5. Note: Community Edition GDS may have limitations on procedure availability

**Q: Is GDS free?**
A: GDS Community is free for development and learning. Note: Community Edition Docker images may have limited procedure availability. For production use or full GDS access, deploy Neo4j Enterprise Edition (requires license).

**Q: Do I need GDS for Lessons 04-05?**
A: No! Those use NetworkX (local Python graphs). GDS is only for Lesson 11+.

**Q: Can I work offline?**
A: First startup needs internet (to download plugin). After that, Docker runs locally.

---

## Verification Checklist

Before starting Lesson 11, verify all components:

- [ ] Docker running: `docker ps` shows `pe-graph-neo4j`
- [ ] Neo4j responsive: Check browser at http://localhost:7474
- [ ] GDS loaded: Lesson 11 Cell 6 shows version number
- [ ] Document_policy graph loaded: Lesson 11 Cell 7 shows 133 nodes
- [ ] Python client working: Can import `from graphdatascience import GraphDataScience`

---

## Next Steps

Once verified, proceed to **Lesson 11: Neo4j Graph Data Science Workflow**

**Run cells in order:**
1. Cell 1: Title & objectives
2. Cell 3: Imports
3. Cell 4: Neo4j connection
4. Cell 6: GDS initialization ← **Check for ✓ message**
5. Cell 7: Dataset verification ← **Confirm 133 nodes**
6. Continue with rest of lesson

---

## Performance Tips

- **Memory**: GDS uses 200-500 MB for document_policy graph
- **CPU**: Parallelized across all cores (faster on multi-core systems)
- **Disk**: SSD recommended for best performance
- **Network**: No internet needed after first startup

---

## Resources

- [Neo4j GDS Documentation](https://neo4j.com/docs/graph-data-science/current/)
- [GDS Python Client](https://python-client.graphdatascience.ai/)
- [Neo4j Community Edition](https://neo4j.com/download-center/)

---

## Support

If still having issues:

1. **Check Docker logs**:
   ```bash
   docker compose logs neo4j | grep -i gds
   ```

2. **Verify Neo4j connectivity**:
   ```bash
   # In notebook
   from neo4j import GraphDatabase
   driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "your_password_here"))
   with driver.session() as session:
       result = session.run("RETURN 'Connected!'")
       print(result.single())
   ```

3. **Test GDS directly**:
   ```bash
   # In notebook
   from graphdatascience import GraphDataScience
   gds = GraphDataScience("bolt://localhost:7687", auth=("neo4j", "your_password_here"))
   print(gds.version())
   ```

---

**Last Updated**: May 22, 2026
**Course**: Graph Analysis for Enterprise Decision-Making
