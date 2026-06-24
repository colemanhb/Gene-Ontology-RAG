import requests
import yaml
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

GITHUB_API = (
    "https://api.github.com/repos/"
    "OBOFoundry/OBOFoundry.github.io/contents/ontology"
)

def load_all_metadata():
    files = requests.get(GITHUB_API).json()

    ontologies = []

    for file in files:
        if not file["name"].endswith(".md"):
            continue

        raw_url = file["download_url"]

        text = requests.get(raw_url).text

        try:
            _, yaml_text, body = text.split("---", maxsplit=2)
        except ValueError:
            continue

        metadata = yaml.safe_load(yaml_text)
        metadata["body"] = body.strip()

        ontologies.append(metadata)

    return ontologies


def create_documents(ontologies):
    docs = []

    for ontology in ontologies:
        content = f"""
Title: {ontology.get('title', '')}

Description:
{ontology.get('description', '')}

Details:
{ontology.get('body', '')}
"""

        docs.append(
            Document(
                page_content=content.strip(),
                metadata={
                    "id": ontology.get("id"),
                    "title": ontology.get("title"),
                    "prefix": ontology.get("preferredPrefix"),
                    "domain": ontology.get("domain"),
                    "repository": ontology.get("repository"),
                    "homepage": ontology.get("homepage"),
                    "activity_status": ontology.get("activity_status"),
                },
            )
        )

    return docs

def build_qdrant_index(docs):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    client = QdrantClient(":memory:")

    vectorstore = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        client=client,
        collection_name="obo_ontologies",
    )

    return vectorstore

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)