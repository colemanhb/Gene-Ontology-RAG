from ingestion.bioportal import (
    load_all_metadata,
    make_blob,
)
from embeddings.client import LlamaCppEmbeddingClient

ontologies = load_all_metadata()

ontology = ontologies[0]

blob = make_blob(ontology)

embedder = LlamaCppEmbeddingClient()
embedding = embedder.embed(blob)

print("Success!")