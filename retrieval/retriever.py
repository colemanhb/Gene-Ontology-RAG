import numpy as np

from embeddings.client import LlamaCppEmbeddingClient
from vectorstore.turbovec_index import TurboVecIndex
from db.postgres import get_conn

from psycopg2.extras import RealDictCursor


class OntologyRetriever:

    def __init__(
        self,
        index_path="data/ontology_index.tvim",
        embedding_dim=384,
    ):
        self.embedder = LlamaCppEmbeddingClient()

        self.index = TurboVecIndex.load(
            index_path,
            dim=embedding_dim,
        )

    def retrieve(self, query, k=5):
        query_vector = self.embedder.embed(query)

        scores, ids = self.index.search(query_vector, k=k)

        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        results = []

        for score, ontology_id in zip(scores, ids):
            cur.execute(
                """
                SELECT *
                FROM ontologies
                WHERE id = ANY(%s)
                """,
                (list(map(int, ids)),)
            )

            row = cur.fetchall()

            if row is not None:
                results.append({
                    "score": float(score),
                    "ontology": row,
                })

        cur.close()
        conn.close()

        return results