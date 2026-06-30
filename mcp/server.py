from mcp.server.fastmcp import FastMCP
from retrieval.retriever import OntologyRetriever

mcp = FastMCP("Ontology Search")

retriever = OntologyRetriever()

@mcp.tool()
def search_ontology(question: str):
    """Search BioPortal ontologies."""

    return retriever.retrieve(question)

if __name__ == "__main__":
    mcp.run()