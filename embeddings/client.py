# embeddings/client.py

from urllib import response

import requests
import numpy as np

class LlamaCppEmbeddingClient:
    def __init__(self, url="http://localhost:8081"):
        self.url = url

    def embed(self, text: str):
        response = requests.post(
            f"{self.url}/embeddings",
            json={"input": text}
        )

        response.raise_for_status()

        data = response.json()
        
        embedding = data[0]["embedding"][0]

        return np.asarray(embedding, dtype=np.float32)

    def embed_batch(self, texts):
        return np.vstack([self.embed(t) for t in texts])

    def embed_query(self, text: str):
        return self.embed(text)