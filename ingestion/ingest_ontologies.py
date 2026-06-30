import numpy as np

from ingestion.bioportal import (
    load_all_metadata,
    make_blob,
)

from embeddings.client import LlamaCppEmbeddingClient
from vectorstore.turbovec_index import TurboVecIndex

from db.postgres import (
    init_db,
    insert_ontology,
)

INDEX_PATH = "data/ontology_index.tvim"


def main():

    print("Initializing database...")
    init_db()

    print("Loading BioPortal metadata...")
    ontologies = load_all_metadata()

    print(f"Found {len(ontologies)} ontologies.")

    embedder = LlamaCppEmbeddingClient()

    vectors = []
    ids = []

    for ontology in ontologies:

        blob = make_blob(ontology)

        blob = blob[:1000]  # truncate to 10k characters

        print(f"Embedding {ontology['id']}")
        print(f"Blob length: {len(blob)}")

        postgres_id = insert_ontology(
            acronym=ontology["id"],
            title=ontology["name"],
            abstract=ontology["description"],
            full_text=blob,
        )

        embedding = embedder.embed(blob)

        vectors.append(embedding)
        ids.append(postgres_id)

        print(f"Indexed {ontology['id']}")

    vectors = np.asarray(vectors, dtype=np.float32)
    ids = np.asarray(ids, dtype=np.uint64)

    print("Building TurboVec index...")

    index = TurboVecIndex(
        dim=vectors.shape[1]
    )

    index.build(vectors, ids)

    index.save(INDEX_PATH)

    print("Done.")

if __name__ == "__main__":
    main()