from mcp.server.fastmcp import FastMCP
from retrieval.retriever import OntologyRetriever

mcp = FastMCP(
    "Ontology Search",
    instructions="Search BioPortal ontologies using semantic retrieval.",
    )
retriever = OntologyRetriever()

@mcp.tool()
def search_ontology(question: str):
    """Search BioPortal ontologies."""
    results =  retriever.retrieve(question)
    return [
        {
            "score": result["score"],
            "acronym": result["ontology"]["acronym"],
            "title": result["ontology"]["title"],
            "abstract": result["ontology"]["abstract"],
        }
        for result in results
    ]

app = mcp.streamable_http_app()