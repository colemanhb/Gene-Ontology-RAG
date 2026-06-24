from load_metadata import *

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
llm = LlamaCpp(
    model_path="/Users/colemanhall-brown/.cache/huggingface/hub/models--google--gemma-4-12B-it-qat-q4_0-gguf/snapshots/f6e7774e6148da3b7f201e42ba37cf084c1db35f/gemma-4-12b-it-qat-q4_0.gguf",
    temperature=0,
    max_tokens=256,
    n_ctx=4096,
)

PERSIST_PATH = "./qdrant_db"
COLLECTION_NAME = "ontology-metadata"

def main():
    client = QdrantClient(path=PERSIST_PATH)

    collection_exists = False

    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        collection_exists = True
    except Exception:
        client.close()

    if collection_exists:
        print("Loading existing collection...")
        
        vectorstore = QdrantVectorStore(
            collection_name=COLLECTION_NAME,
            embedding=embeddings,
            client=client,
        )
    
    else:
        print("Building new collection...")

        ontologies = load_all_metadata()
        docs = create_documents(ontologies)
        
        vectorstore = QdrantVectorStore.from_documents(
            docs,
            embedding=embeddings,
            path=PERSIST_PATH,
            collection_name=COLLECTION_NAME,
        )


    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    
    template = """
    You are a biomedical ontology recommender.

    Use only information found in the retrieved ontology metadata.

    If the metadata does not contain enough information to answer the question,
    say "I do not have enough information in the ontology metadata to answer."

    Context:
    {context}

    User question: 
    {question}

    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n--- The Ontology Query Machine is ready to answer your questions ---")
    while True: 
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break

        response = rag_chain.invoke(query)
        print(f"\nOntology Querier: {response}")

if __name__ == "__main__":
    main()
