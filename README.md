This is a RAG for querying the different biomedical ontologies available in OBO foundry.

# Project Workflow

```text
                         INGESTION PIPELINE

┌──────────────────────────────────────────────────────────────┐
│ BioPortal API                                                │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
Download ontology metadata
📁 ingestion/bioportal.py
    • load_all_metadata()
    • _safe_get()
                            │
                            ▼
Create ontology text blob
📁 ingestion/bioportal.py
    • make_blob()
                            │
                            ▼
Store ontology metadata
📁 db/postgres.py
    • insert_ontology()
    • PostgreSQL table
                            │
                            ▼
Generate embedding
📁 embeddings/client.py
    • LlamaCppEmbeddingClient
    • POST /embeddings
    • llama.cpp embedding server
                            │
                            ▼
Store embedding in TurboVec
📁 vectorstore/turbovec_index.py
    • add_with_ids()
    • IdMapIndex
                            │
                            ▼
Save TurboVec index
📁 data/
    • ontology_index.tvim

────────────────── Ingestion Complete ──────────────────

                         RETRIEVAL PIPELINE

User Question
                            │
                            ▼
Embed user query
📁 embeddings/client.py
                            │
                            ▼
Similarity search
📁 vectorstore/turbovec_index.py
    • search()
                            │
                            ▼
Top matching ontology IDs
                            │
                            ▼
Lookup metadata by ID
📁 db/postgres.py
                            │
                            ▼
Retriever assembles results
📁 retrieval/retriever.py
                            │
                            ▼
Return best matching ontologies
```

## Directory Responsibilities

| Directory | Responsibility |
|-----------|----------------|
| `ingestion/` | Downloads ontology metadata from BioPortal and creates text blobs for embedding. |
| `embeddings/` | Sends text to the local llama.cpp embedding server and receives embedding vectors. |
| `db/` | Stores ontology metadata and maps ontology IDs to database records. |
| `vectorstore/` | Stores compressed embedding vectors in TurboVec and performs nearest-neighbor search. |
| `retrieval/` | Combines embeddings, TurboVec, and PostgreSQL to answer user queries. |
| `scripts/` | Testing and maintenance utilities (`test_db.py`, `test_embeddings.py`, `test_retrieval.py`, `reset_db.py`). |
| `data/` | Stores generated TurboVec index files. |