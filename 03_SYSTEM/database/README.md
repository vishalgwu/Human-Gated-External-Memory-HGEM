# HGEM Database Layer

Database responsibilities:

- PostgreSQL: T1 immutable constants, experiment events, conflict logs.
- Neo4j: T2 human-validated graph memory.
- Redis: T3 rolling five-turn ephemeral memory.
- ChromaDB: vector measurement index only, never HGEM retrieval context.

