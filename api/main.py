from fastapi import FastAPI
from pydantic import BaseModel

from retrieval.retriever import OntologyRetriever

app = FastAPI()

retriever = OntologyRetriever()


class SearchRequest(BaseModel):
    question: str


@app.post("/search")
def search(req: SearchRequest):

    results = retriever.retrieve(req.question)

    return results