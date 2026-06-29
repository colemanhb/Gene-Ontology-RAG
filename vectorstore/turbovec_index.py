# vectorstore/turbovec_index.py

import numpy as np
from turbovec import IdMapIndex

class TurboVecIndex:
    def __init__(self, dim: int, bit_width: int = 4):
        self.index = IdMapIndex(dim=dim, bit_width=bit_width)
        self.id_map = {}  # postgres_id → metadata (optional cache)

    def build(self, vectors: np.ndarray, ids: np.ndarray):
        """
        vectors: (N, dim)
        ids: (N,) postgres IDs
        """
        self.index.add_with_ids(vectors, ids)

    def search(self, query_vec: np.ndarray, k: int = 5):
        scores, ids = self.index.search(
            np.asarray([query_vec], dtype=np.float32),
            k=k
        )
        return scores[0], ids[0]

    def save(self, path: str):
        self.index.write(path)

    @classmethod
    def load(cls, path: str, dim: int):
        obj = cls(dim)
        obj.index = IdMapIndex.load(path)
        return obj