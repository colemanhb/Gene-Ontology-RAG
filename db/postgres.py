# db/postgres.py

import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "obo",
    "user": "colemanhall-brown",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create ontology table"""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ontologies (
        id SERIAL PRIMARY KEY,
        acronym TEXT UNIQUE,
        title TEXT,
        abstract TEXT,
        full_text TEXT,
        category TEXT,
        vector_id BIGINT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


def insert_ontology(
    acronym,
    title,
    abstract,
    full_text,
    category=None,
    vector_id=None  # 🆕 TurboVec ID hook
):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        INSERT INTO ontologies (
            acronym,
            title,
            abstract,
            full_text,
            category,
            vector_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (acronym)
        DO UPDATE SET
            title = EXCLUDED.title,
            abstract = EXCLUDED.abstract,
            full_text = EXCLUDED.full_text,
            category = EXCLUDED.category,
            vector_id = EXCLUDED.vector_id
        RETURNING id;
    """, (
        acronym,
        title,
        abstract,
        full_text,
        category,
        vector_id
    ))

    row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if not row:
        raise RuntimeError(f"Insert failed for ontology: {acronym}")

    return row["id"]


def fetch_all_ontologies():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM ontologies;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

def clear_ontologies():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("TRUNCATE TABLE ontologies RESTART IDENTITY;")

    conn.commit()
    cur.close()
    conn.close()

def fetch_ontology(id):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM ontologies
        WHERE id=%s
        """,
        (id,),
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row