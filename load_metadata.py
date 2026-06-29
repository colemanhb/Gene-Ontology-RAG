import requests
from llama_index.core import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from qdrant_client import QdrantClient

API_KEY = "622683ad-2781-4efd-96b6-af9c82bf31d6"

HEADERS = {
    "Authorization": f"apikey token={API_KEY}"
}

ONTOLOGY_URL = "https://data.bioontology.org/ontologies"

def load_all_metadata():
    ontologies = []

    response = requests.get(ONTOLOGY_URL, headers=HEADERS)
    response.raise_for_status()

    for ontology in response.json():
        ontologies.append({
            "id": ontology.get("acronym"),
            "title": ontology.get("name"),
            "abstract": ontology.get("description"),
            "homepage": ontology.get("homepage"),
            "version": ontology.get("version"),
            "status": ontology.get("status"),
            "viewOf": ontology.get("viewOf"),
            "categories": [
                c["acronym"] for c in ontology.get("hasDomain", [])
            ],
        })

    return ontologies


def create_documents(ontologies):
    docs = []

    for ontology in ontologies:
        content = f"""
        Title: {ontology.get('title', '')}

        Acronym:
        {ontology.get("id")}

        Abstract:
        {ontology.get('abstract', '')}

        Categories:
        {", ".join(ontology.get("categories", []))}

        Homepage:
        {ontology.get('homepage', '')}

        Version:
        {ontology.get('version', '')}
        """

        docs.append(
            Document(
                text=content.strip(),
                metadata={
                    "id": ontology["id"],
                    "title": ontology["title"],
                    "homepage": ontology["homepage"],
                    "version": ontology["version"],
                    "categories": ontology["categories"],
                },
            )
        )

    return docs

def build_qdrant_index(docs):
    client = QdrantClient(":memory:")

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="obo_ontologies",
    )

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    index = VectorStoreIndex.from_documents(
        docs,
        storage_context=storage_context,
    )

    return index

def format_docs(docs):
    return "\n\n".join(doc.text for doc in docs)