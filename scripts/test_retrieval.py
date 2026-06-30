from retrieval.retriever import OntologyRetriever


def main():

    retriever = OntologyRetriever()

    while True:

        query = input("\nQuestion: ")

        if query.lower() in ("quit", "exit"):
            break

        results = retriever.retrieve(query)

        print()

        for result in results:
            ontology = result["ontology"]
            print("=" * 60)
            print(f"Similarity: {result['score']:.3f}")
            print(f"Acronym:   {ontology['acronym']}")
            print(f"Title:     {ontology['title']}")
            print(f"Category:  {ontology['category']}")
            print(f"Abstract:  {ontology['abstract']}")
            print()


if __name__ == "__main__":
    main()