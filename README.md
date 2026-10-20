# Library SQL Quiz

A web-based SQL quiz built with Streamlit and hosted PostgreSQL through Supabase. Students can create accounts, sign in, execute SQL queries against a live database, view query results, and save their answers.

## Live Application

**[Open the Library SQL Quiz](https://library-sql-quiz-jyhzfd9nbcsttdshxzxtrh.streamlit.app/)**

**GitHub Repository:** https://github.com/Nada-a-ali/library-sql-quiz

## Project Features

- Student registration and sign-in using Supabase Authentication
- Five SQL questions worth four points each (20 points total)
- Questions covering filtering, aggregation, joins, Common Table Expressions (CTEs), and window functions
- Hints containing expected SQL queries and expected results
- Interactive SQL editor for each question
- Execution of read-only SQL queries against hosted PostgreSQL
- Query results displayed as tables
- Ability for authenticated students to save and update SQL answers
- Database reference listing available tables and columns
- GitHub Actions workflow using GitHub Secrets

## Database

The application uses PostgreSQL hosted through Supabase.

The library dataset contains three main tables:

| Table | Description |
|---|---|
| `books` | Book titles, authors, genres, publication years, and ratings |
| `members` | Library member information |
| `borrowings` | Records linking members to borrowed books |

Additional database tables store quiz questions, student-facing question information, and student submissions.

## Quiz Structure

| Question | Topics | Points |
|---|---|---|
| 1 | Filtering and sorting | 4 |
| 2 | Aggregation, GROUP BY, HAVING | 4 |
| 3 | JOIN and aggregation | 4 |
| 4 | CTE, JOIN, and aggregation | 4 |
| 5 | Multiple CTEs and DENSE_RANK | 4 |
| **Total** | | **20** |

## How to Use the Application

1. Open the deployed Streamlit application.
2. Create an account or sign in with an existing account.
3. Expand the Database Reference to review the available tables and columns.
4. Select one of the five quiz questions.
5. Write an SQL query in the provided editor.
6. Click **Run Query** to execute the query and display its results.
7. Expand **Show Expected SQL and Result** to review the expected answer.
8. Click **Save Answer** to store or update your submission.

Quiz access, SQL execution, and answer saving require authentication.

## Local Setup

Clone the repository:

```bash
git clone https://github.com/Nada-a-ali/library-sql-quiz.git
cd library-sql-quiz
```

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file containing:

```text
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_publishable_key
DATABASE_URL=your_postgresql_connection_url
QUIZ_DB_PASSWORD=your_restricted_database_password
```

The application uses a restricted PostgreSQL account for executing quiz queries. The database URL must provide valid connection details for the Supabase PostgreSQL pooler.

The `.env` file is excluded from Git using `.gitignore`. Credentials must not be committed to the repository.

Run the application:

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal.

## Authentication and Database Security

Supabase Authentication manages student accounts and sign-in.

Student submissions use Row Level Security policies so authenticated users can save and access their own answers. SQL queries are executed through a restricted PostgreSQL account using read-only transactions and query timeouts.

## GitHub Actions

The repository includes an automated workflow:

`.github/workflows/database-check.yml`

The workflow runs on pushes and can also be triggered manually. It connects to the hosted PostgreSQL database using the restricted account and verifies the expected library and quiz-question counts.

The connection string is stored securely in the GitHub Actions repository secret:

`QUIZ_DATABASE_URL`

A successful workflow run has been verified in GitHub Actions.

## Deployment

The application is deployed using Streamlit Community Cloud and connected to this GitHub repository.

Deployment credentials are configured through Streamlit's private app secrets rather than being stored in source code.

**Live website:** https://library-sql-quiz-jyhzfd9nbcsttdshxzxtrh.streamlit.app/