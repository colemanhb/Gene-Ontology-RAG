from db.postgres import *

def main():
    print("Initializing DB...")
    init_db()

    print("Inserting test row...")
    oid = insert_ontology(
        acronym="TEST",
        title="Test Ontology",
        abstract="This is a fake ontology for testing.",
        full_text="Test Ontology full text blob",
        category="test"
    )

    print("Inserted ID:", oid)

    rows = fetch_all_ontologies()
    print("\nRows in DB:")
    for r in rows:
        print(r)

    print("\nClearing ontologies table...")
    clear_ontologies()

if __name__ == "__main__":
    main()