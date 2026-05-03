# ChromaDB Setup

ChromaDB is used for drift measurement only.

Important research rule: ChromaDB embeddings must not be used to retrieve HGEM context for the model. Context injection for the full HGEM condition comes from T1 plus Neo4j graph traversal plus T3.

Default local persist directory:

```text
03_SYSTEM/database/chromadb/chroma_store
```

