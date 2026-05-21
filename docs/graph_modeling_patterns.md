# Graph Modeling Patterns

## Common Entity-Relationship Patterns

### 1. Hierarchical/Tree Structure

**Example**: Organization chart, categories, taxonomy

```
        CEO
        |
    +---+---+
    |       |
   CTO    CFO
    |       |
  Eng    Finance
```

**Graph Model**:
```
(Person)-[:REPORTS_TO]->(Manager)
(Category)-[:PARENT_OF]->(Subcategory)
```

**Queries**:
- Find direct reports: `MATCH (m:Person)-[:REPORTS_TO]-(emp:Person)`
- Find all subordinates: `MATCH path = (m:Person)-[:REPORTS_TO*]->(emp:Person)`

---

### 2. Bipartite Networks

**Example**: Users-Topics, Customers-Products, People-Skills

```
Users          Topics
Alice  ------>  Python
  |  \------>  Graphs
Bob   ------->  ML
  |  \------>  Python
```

**Graph Model**:
```
(User)-[:INTERESTED_IN]->(Topic)
(Customer)-[:PURCHASED]->(Product)
```

**Queries**:
- Users interested in Python: `MATCH (:User)-[:INTERESTED_IN]-(t:Topic {name: 'Python'})`
- Topic overlap: `MATCH (u1:User)-[:INTERESTED_IN]->(t:Topic)<-[:INTERESTED_IN]-(u2:User)`

---

### 3. Social Network

**Example**: People connecting to people, followers, collaborations

```
Alice ---friends---> Bob
  |                   |
  +---> Charlie <----+
```

**Graph Model**:
```
(Person)-[:FOLLOWS]->(Person)
(Person)-[:FRIEND_OF]->(Person)  // Often symmetric
(Person)-[:COLLABORATED_WITH]->(Person)
```

**Queries**:
- Friends of friends: `MATCH (p:Person)-[:FRIEND_OF]->()-[:FRIEND_OF]->(fof:Person)`
- Common friends: `MATCH (a:Person)-[:FRIEND_OF]-(mutual)-[:FRIEND_OF]-(b:Person)`

---

### 4. Approval/Workflow Process

**Example**: Approval chains, request routing, state machines

```
Request → Submitted → Manager → CFO → Approved
            Review    Review   Review
```

**Graph Model**:
```
(Request)-[:SUBMITTED_BY]->(User)
(Request)-[:ASSIGNED_TO]->(Approver)
(Request)-[:CURRENT_STATE]->(State)
(User)-[:REPORTS_TO]->(Manager)
(State)-[:NEXT_STATE]->(State)
```

**Queries**:
- Bottlenecks: `MATCH (s:State)<-[:CURRENT_STATE]-(r:Request) WHERE ... RETURN s, count(r)`
- Approval paths: `MATCH path = (r:Request)-[:ASSIGNED_TO]->()* RETURN path`

---

### 5. Dependency/Constraint Network

**Example**: Software dependencies, project dependencies, system architecture

```
ServiceA --- depends_on ---> ServiceB
              depends_on
                    |
                    v
                ServiceC
```

**Graph Model**:
```
(Service)-[:DEPENDS_ON]->(Service)
(Component)-[:REQUIRES]->(Library)
(Task)-[:BLOCKED_BY]->(Task)
```

**Queries**:
- Find all dependencies: `MATCH path = (s:Service)-[:DEPENDS_ON*]->(dep:Service) RETURN path`
- Circular dependencies: Look for cycles in dependency graph
- Impact analysis: Reverse direction to find what depends on changed component

---

### 6. Document/Knowledge Graph

**Example**: Documents referencing policies, wikis, knowledge bases

```
Document A
  ├─ references → Document B
  ├─ about → Topic
  └─ owned_by → Person
```

**Graph Model**:
```
(Document)-[:REFERENCES]->(Document)
(Document)-[:ABOUT]->(Topic)
(Document)-[:OWNED_BY]->(Person)
(Topic)-[:SUPERSEDES]->(Topic)  // Deprecated docs
```

**Queries**:
- Related documents: `MATCH (d1:Document)-[:REFERENCES*]-(d2:Document) RETURN d1, d2`
- Orphaned docs: `MATCH (d:Document) WHERE NOT (d)-[:OWNED_BY]->() RETURN d`
- Scope of change: `MATCH (d:Document)-[:REFERENCES*]-(changed:Document) RETURN d`

---

### 7. Event/Timeline Graph

**Example**: Incidents, support tickets, event sequences

```
Ticket (created) → Event1 → Event2 → Event3 (resolved)
          |                    |
          +---assigned_to----→ Agent
                               |
                          worked_on
```

**Graph Model**:
```
(Ticket)-[:HAS_EVENT]->(Event)
(Event)-[:NEXT_EVENT]->(Event)
(Event)-[:ASSIGNED_TO]->(Agent)
(Ticket)-[:CREATED_BY]->(Customer)
(Ticket)-[:RESOLVED_BY]->(Agent)
```

**Queries**:
- Timeline: `MATCH path = (t:Ticket)-[:HAS_EVENT]-(:Event)-[:NEXT_EVENT*]->(:Event) RETURN path`
- Event sequences: `MATCH (e1:Event)-[:NEXT_EVENT*]->(e2:Event) RETURN e1, e2`
- Time to resolution: Compute from created timestamp to resolved timestamp

---

### 8. Supplier/Partner Network

**Example**: Companies, suppliers, partners, agreements

```
Company A --- supplies --> Company B
         \ --- partners_with --> Company C
         \ --- conflicts_with --> Company D
```

**Graph Model**:
```
(Company)-[:SUPPLIES]->(Company)
(Company)-[:PARTNERS_WITH]->(Company)
(Company)-[:COMPETES_WITH]->(Company)
(Company)-[:OWNS]->(Subsidiary)
```

**Queries**:
- Supply chain: `MATCH path = (buyer:Company)-[:SUPPLIES*]-(supplier:Company) RETURN path`
- Risk analysis: Find if competitors are in supply chain
- Diversification: `MATCH (c:Company)-[:SUPPLIES]-(sup) RETURN c, count(sup) as suppliers`

---

## Design Guidelines

1. **Use relationships to encode business logic** — Not just attributes
2. **Denormalize strategically** — Add redundant properties on nodes for fast queries
3. **Version entities when they change** — Keep history in graph
4. **Label nodes by function, not just type** — Use properties for additional classification
5. **Index on frequently queried properties** — Essential for performance
6. **Use relationship types as semantic layers** — Different edge types = different business meanings

## Anti-Patterns to Avoid

- ❌ Storing relationships as node attributes (e.g., "friend_ids" as string)
- ❌ Using undirected edges when direction has meaning
- ❌ Creating too many relationship types (pollutes the schema)
- ❌ Overloading node/edge attributes instead of using relationships
- ❌ Not using constraints for uniqueness (leads to duplicates)
