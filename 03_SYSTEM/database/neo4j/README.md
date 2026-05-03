# Neo4j Setup

Neo4j stores T2 human-validated memory as a graph.

Run the initialization script after Neo4j is available:

```powershell
cypher-shell -u neo4j -p <password> -f 01_SETUP/neo4j_config/init.cypher
```

Validated memory nodes use label `ValidatedNode`. The four required edge types are `DEPENDS_ON`, `LEADS_TO`, `CONTRADICTS`, and `CONFIRMS`.

