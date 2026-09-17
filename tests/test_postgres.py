import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRES_DB"),
    sslmode="require"
)

print("✅ PostgreSQL connection successful")

with conn.cursor() as cur:
    cur.execute("SHOW azure.extensions;")
    print("Allowed extensions:", cur.fetchone()[0])

    cur.execute("""
        SELECT current_user,
               pg_has_role(current_user, 'azure_pg_admin', 'member');
    """)
    print("User / azure_pg_admin:", cur.fetchone())

conn.close()