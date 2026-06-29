import numpy as np

from load_metadata import load_all_metadata, create_documents

from turbovec import IdMapIndex

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.core.prompts import PromptTemplate

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

llm = LlamaCPP(
    model_path="/Users/colemanhall-brown/.cache/huggingface/hub/models--google--gemma-4-12B-it-qat-q4_0-gguf/snapshots/f6e7774e6148da3b7f201e42ba37cf084c1db35f/gemma-4-12b-it-qat-q4_0.gguf",
    temperature=0,
    max_new_tokens=256,
    context_window=4096,
)

PERSIST_PATH = "./vector_db"
COLLECTION_NAME = "ontology-metadata"

def main():
    qa_prompt = PromptTemplate(
    """
    Use only retrieved BioPortal ontology metadata.

    Recommend the ontology or ontologies that best answer the user's question by telling them the name and abbreviation of the ontology.
    If recommending multiple ontologies, do not recommend the same one more than once.
    Explain your reasoning using only the retrieved metadata. 

    If the metadata does not contain enough information to answer the question or none of the retrieved ontologies are appropriate,
    say that you do not have enough information.

    Context:
    {context_str}

    Question: 
    {query_str}

    Answer:"""
    )

    ontologies = load_all_metadata()
    docs = create_documents(ontologies)

    # ---- EMBEDDINGS ----
    embeddings = embed_model.get_text_embedding_batch(
        [doc.text for doc in docs]
    )

    vectors = np.asarray(embeddings, dtype=np.float32)

    # ---- TURBOVEC INDEX ----
    index = IdMapIndex(
        dim=vectors.shape[1],
        bit_width=4,
    )

    ids = np.arange(len(docs), dtype=np.uint64)
    index.add_with_ids(vectors, ids)

    # ---- LOOKUP TABLE ----
    doc_lookup = {i: doc for i, doc in enumerate(docs)}

    print("\n--- Ready ---")

    while True:
        query = input("\nYou: ")
        if query.lower() in ["quit", "exit"]:
            break

        # ---- QUERY EMBEDDING ----
        q_emb = embed_model.get_query_embedding(query)

        scores, top_ids = index.search(
            np.asarray([q_emb], dtype=np.float32),
            k=3,
        )

        retrieved_docs = [
            doc_lookup[int(i)] for i in top_ids[0]
        ]

        context = "\n\n".join(doc.text for doc in retrieved_docs)

        prompt = qa_prompt.format(
            context_str=context,
            query_str=query
        )

        response = llm.complete(prompt)

        print("\nOntology Querier:", response.text)