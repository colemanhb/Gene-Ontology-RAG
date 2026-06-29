# db/drop_db.py

from db.postgres import get_conn


def main():
    conn = get_conn()
    cur = conn.cursor()

    print("Dropping ontologies table...")

    cur.execute("""
        DROP TABLE IF EXISTS ontologies CASCADE;
    """)

    conn.commit()

    cur.close()
    conn.close()

    print("Done.")


if __name__ == "__main__":
    main()