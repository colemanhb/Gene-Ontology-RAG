# scripts/test_turbovec.py

import numpy as np

from embeddings.client import LlamaCppEmbeddingClient
from vectorstore.turbovec_index import TurboVecIndex


def main():
    print("Initializing embedding client...")
    embedder = LlamaCppEmbeddingClient("http://localhost:8081")

    print("Creating sample ontology documents...")

    docs = [
        (
            101,
            """
            Title: Gene Ontology

            Abstract:
            Describes gene products using molecular function,
            biological process, and cellular component.
            """
        ),
        (
            102,
            """
            Title: Human Phenotype Ontology

            Abstract:
            Describes human phenotypic abnormalities and diseases.
            """
        ),
        (
            103,
            """
            Title: ChEBI

            Abstract:
            Ontology of chemical entities of biological interest.
            """
        ),
        (
            104,
            """
            Title: Plant Ontology

            Abstract:
            Describes plant anatomy and developmental stages.
            """
        ),
    ]

    print("Embedding documents...")

    vectors = []
    ids = []

    for doc_id, text in docs:
        vectors.append(embedder.embed(text))
        ids.append(doc_id)

    vectors = np.asarray(vectors, dtype=np.float32)
    ids = np.asarray(ids, dtype=np.uint64)

    print(f"Vector matrix shape: {vectors.shape}")

    print("Building TurboVec index...")

    index = TurboVecIndex(dim=vectors.shape[1])
    index.build(vectors, ids)

    print("Running similarity search...")

    query = "ontology describing genes and biological processes"

    query_vec = embedder.embed(query)

    scores, results = index.search(query_vec, k=3)

    print("\nQuery:")
    print(query)

    print("\nNearest neighbors:")

    for score, doc_id in zip(scores, results):
        print(f"ID={int(doc_id):3d}   score={score:.4f}")

    print("\nSaving index...")

    index.save("ontology_index.tvim")

    print("Reloading index...")

    loaded = TurboVecIndex.load(
        "ontology_index.tvim",
        dim=vectors.shape[1]
    )

    scores, results = loaded.search(query_vec, k=3)

    print("\nResults after reload:")

    for score, doc_id in zip(scores, results):
        print(f"ID={int(doc_id):3d}   score={score:.4f}")

    print("\nTurboVec test complete.")


if __name__ == "__main__":
    main()