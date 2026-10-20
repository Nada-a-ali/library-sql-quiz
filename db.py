import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    admin_info = psycopg.conninfo.conninfo_to_dict(os.environ["DATABASE_URL"])

    project_ref = os.environ["SUPABASE_URL"].split("//")[1].split(".")[0]

    return psycopg.connect(
        host=admin_info["host"],
        port=admin_info.get("port", "5432"),
        dbname=admin_info.get("dbname", "postgres"),
        user=f"quiz_app.{project_ref}",
        password=os.environ["QUIZ_DB_PASSWORD"],
        sslmode="require",
        connect_timeout=10,
    )


def get_questions():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT question_id, question_text, points, hint
                FROM public.student_questions
                ORDER BY question_id
            """)

            return cur.fetchall()


def run_student_query(query):
    """Execute one read-only SQL query against PostgreSQL."""

    query = query.strip()

    if not query:
        raise ValueError("Please enter a SQL query.")

    with get_connection() as conn:
        # Read-only transaction prevents database changes.
        with conn.transaction():
            conn.execute("SET TRANSACTION READ ONLY")
            conn.execute("SET LOCAL statement_timeout = '5000ms'")

            with conn.cursor() as cur:
                cur.execute(query, prepare=False)

                if cur.description is None:
                    raise ValueError("Your query must return a result table.")

                columns = [column.name for column in cur.description]
                rows = cur.fetchmany(501)

                if len(rows) > 500:
                    raise ValueError("Too many rows. Add LIMIT 500 to your query.")

                return columns, rows
