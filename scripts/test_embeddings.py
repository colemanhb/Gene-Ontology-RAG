from embeddings.client import LlamaCppEmbeddingClient
import numpy as np


def main():
    print("Initializing embedding client...")

    # make sure this matches your llama.cpp server port
    client = LlamaCppEmbeddingClient("http://localhost:8081")

    test_texts = [
        "ontology describing metabolic processes",
        "gene regulation in biological systems",
        "cellular respiration and energy production"
    ]

    print("\nEmbedding test texts...\n")

    vectors = []

    for text in test_texts:
        vec = client.embed(text)
        vectors.append(vec)

        print(f"Text: {text}")
        print(f"Vector shape: {vec.shape}")
        print(f"First 5 values: {vec[:5]}")
        print("-" * 50)

    # ---- sanity checks ----
    print("\nRunning sanity checks...")

    dims = [v.shape[0] for v in vectors]

    if len(set(dims)) == 1:
        print(f"✅ All embeddings have consistent dimension: {dims[0]}")
    else:
        print("❌ Inconsistent embedding dimensions:", dims)

    # check vector type
    if isinstance(vectors[0], np.ndarray):
        print("✅ Output type is NumPy array")

    # check non-zero vectors
    zero_vectors = [i for i, v in enumerate(vectors) if np.all(v == 0)]
    if not zero_vectors:
        print("✅ No zero vectors detected")
    else:
        print("⚠️ Zero vectors found at indices:", zero_vectors)

    print("\nEmbedding test complete.")


if __name__ == "__main__":
    main()