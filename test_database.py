import os
import psycopg
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is missing from .env")

# Connect to PostgreSQL securely
with psycopg.connect(database_url, connect_timeout=10, sslmode="require") as conn:

    # Run a simple SQL query
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM public.books;")
        book_count = cur.fetchone()[0]

        print("PostgreSQL connection successful!")
        print(f"Number of books: {book_count}")
