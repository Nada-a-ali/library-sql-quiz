import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

# Get the existing Session pooler connection details.
admin_url = os.getenv("DATABASE_URL")
quiz_password = os.getenv("QUIZ_DB_PASSWORD")

if not admin_url or not quiz_password:
    raise ValueError("Missing database configuration in .env")

# Reuse the host, port, and database, but NOT
# the administrator's username or password.
admin_info = psycopg.conninfo.conninfo_to_dict(admin_url)

project_ref = os.getenv("SUPABASE_URL").split("//")[1].split(".")[0]

# Supabase Session pooler uses a project-qualified username.
quiz_username = f"quiz_app.{project_ref}"

connection_info = {
    "host": admin_info["host"],
    "port": admin_info.get("port", "5432"),
    "dbname": admin_info.get("dbname", "postgres"),
    "user": quiz_username,
    "password": quiz_password,
    "sslmode": "require",
    "connect_timeout": 10,
}

try:
    with psycopg.connect(**connection_info) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT current_user;")
            print("Connected as:", cur.fetchone()[0])

            cur.execute("SELECT COUNT(*) FROM public.books;")
            print("Number of books:", cur.fetchone()[0])

    print("Restricted database connection successful!")

except psycopg.Error as error:
    print("Database connection failed.")
    print("Error type:", type(error).__name__)
    print("SQLSTATE:", error.sqlstate)

# Verify permissions without modifying any data
with psycopg.connect(**connection_info) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                has_table_privilege(
                    current_user, 'public.books', 'SELECT'
                ) AS can_read_books,
                has_table_privilege(
                    current_user, 'public.books', 'INSERT'
                ) AS can_insert_books,
                has_table_privilege(
                    current_user, 'public.books', 'UPDATE'
                ) AS can_update_books,
                has_table_privilege(
                    current_user, 'public.books', 'DELETE'
                ) AS can_delete_books,
                has_table_privilege(
                    current_user, 'public.quiz_questions', 'SELECT'
                ) AS can_read_answer_key;
        """)

        permissions = cur.fetchone()
        print("Permissions:", permissions)
