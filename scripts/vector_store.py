import os
import json

import psycopg
from dotenv import load_dotenv

from scripts.ingest import load_documents, chunk_document

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=5432,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
        sslmode="require",
    )


def create_tables():
    conn = get_connection()

    try:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id BIGSERIAL PRIMARY KEY,
                    source TEXT NOT NULL,
                    mnemonic TEXT NOT NULL,
                    application_name TEXT,
                    issue_id TEXT,
                    metadata JSONB,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()

            print("✅ document_chunks table created successfully")

    finally:
        conn.close()


def load_chunks_into_database():
    documents = load_documents()

    all_chunks = []

    for document in documents:
        chunks = chunk_document(document)
        all_chunks.extend(chunks)

    print(f"📄 Documents found: {len(documents)}")
    print(f"🧩 Chunks found: {len(all_chunks)}")

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE document_chunks RESTART IDENTITY;")

            for chunk in all_chunks:

                metadata = chunk["metadata"]

                cur.execute("""
                    INSERT INTO document_chunks (
                        source,
                        mnemonic,
                        application_name,
                        issue_id,
                        metadata,
                        content
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    chunk["source"],
                    metadata.get("mnemonic"),
                    metadata.get("application_name"),
                    metadata.get("issue_id"),
                    json.dumps(metadata),
                    chunk["content"],
                ))

        conn.commit()

        print(f"✅ {len(all_chunks)} chunks inserted into PostgreSQL")

    finally:
        conn.close()


def verify_chunks():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT mnemonic, COUNT(*)
                FROM document_chunks
                GROUP BY mnemonic
                ORDER BY mnemonic;
            """)

            rows = cur.fetchall()

            print("\nChunk distribution:")

            for mnemonic, count in rows:
                print(f"  {mnemonic}: {count}")

    finally:
        conn.close()

if __name__ == "__main__":
    load_chunks_into_database()
    verify_chunks()