# Graph Findings Template

Use this template to document graph analysis findings in a structured way.

---

## Dataset: [Dataset Name]

**Date**: [Date]  
**Analyst**: [Name or notebook number]  
**Graph Type**: [Directed/Undirected, Weighted/Unweighted]

---

## Dataset Overview

### Scope
- **Nodes**: [Count] ([types])
- **Edges**: [Count] ([types])
- **Time Period**: [Start] to [End] (if temporal)
- **Domain**: [Subject area]

### Data Quality
- **Completeness**: [% coverage]
- **Issues Found**: [None / list any data quality issues]
- **Assumptions**: [List any assumptions made]

---

## Graph Profile

| Metric | Value |
|--------|-------|
| Density | [value] |
| Avg Degree | [value] |
| Connected Components | [count] |
| Isolates | [count] |
| Clustering Coefficient | [value] |
| Diameter | [value] |

---

## Key Patterns Discovered

### Pattern 1: [Pattern Name]

**Description**: [What pattern exists?]

**Evidence**:
- [Metric or observation]
- [Metric or observation]

**Implications**:
- [Operational impact]
- [Strategic consideration]
- [Risk or opportunity]

**Recommendation**: [Action to take]

---

### Pattern 2: [Pattern Name]

**Description**: ...
**Evidence**: ...
**Implications**: ...
**Recommendation**: ...

---

## Anomalies & Outliers

### Anomaly 1: [Name]

- **Affected Nodes**: [Which nodes?]
- **Severity**: [High/Medium/Low]
- **Cause**: [Root cause if known]
- **Action**: [Investigation or remediation needed?]

---

## Centrality Analysis

### Top Nodes by Degree Centrality

| Node | Score | Business Meaning |
|------|-------|-----------------|
| [Node] | [Score] | [Why is this important?] |
| [Node] | [Score] | ... |

### Top Nodes by Betweenness Centrality

| Node | Score | Business Meaning |
|------|-------|-----------------|
| [Node] | [Score] | [Bottleneck / broker / critical path] |
| [Node] | [Score] | ... |

---

## Community Structure

**Number of Communities**: [Count]

### Community Details

| ID | Size | Key Nodes | Characteristics |
|----|------|-----------|-----------------|
| 1 | [size] | [top nodes] | [description] |
| 2 | [size] | [top nodes] | [description] |

---

## Recommendations

1. **Short-term**: [Quick action based on findings]
2. **Medium-term**: [Strategic adjustment needed]
3. **Long-term**: [Structural change to consider]

---

## Limitations & Next Steps

### Limitations of This Analysis
- [Data limitation]
- [Analytical limitation]
- [Scope limitation]

### Suggested Follow-up Analysis
- [Additional analysis that would be valuable]
- [Additional data that would help]
- [Different perspective to examine]

---

**Confidence Level**: [High/Medium/Low]  
**Reviewed By**: [Name]  
**Status**: [Draft/Reviewed/Final]
