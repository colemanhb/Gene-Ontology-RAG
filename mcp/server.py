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
    result =  retriever.retrieve(question)
    return [
        {
            "score": result["score"],
            "acronym": result["ontology"]["acronym"],
            "title": result["ontology"]["title"],
            "abstract": result["ontology"]["abstract"],
        }
        for r in result
    ]

def main():
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        path="/mcp",
    )

if __name__ == "__main__":
    main()