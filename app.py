import streamlit as st
import pandas as pd

from auth import show_auth, get_supabase
from db import get_questions, run_student_query

st.set_page_config(
    page_title="Library SQL Quiz",
    layout="wide",
)

st.title("Library SQL Quiz")
st.write("Practice SQL using a live PostgreSQL database.")

st.subheader("Quiz Overview")
st.write("5 Questions | 20 Points")

st.divider()

show_auth()

if st.session_state.get("auth_session"):
    st.subheader("Quiz Questions")

    with st.expander("Database Reference — Tables and Columns"):
        st.write("**books**")
        st.code("id, title, author, genre, publication_year, rating")

        st.write("**members**")
        st.code("member_id, name, join_year")

        st.write("**borrowings**")
        st.code("borrow_id, book_id, member_id, borrow_date")

        st.caption(
            "Use these tables and columns to write your SQL queries. "
            "You can explore the data using SELECT statements."
        )

    try:
        questions = get_questions()

        for question_id, question_text, points, hint in questions:
            with st.expander(f"Question {question_id} — {points} points"):
                st.write(question_text)
                st.info(f"Hint: {hint}")

                sql_query = st.text_area(
                    "Write your SQL query:",
                    key=f"sql_{question_id}",
                    height=150,
                    placeholder="Write your SQL query here...",
                )

                if st.button("Run Query", key=f"run_{question_id}"):
                    try:
                        session = st.session_state.get("auth_session")
                        supabase = get_supabase()

                        user_response = supabase.auth.get_user(session.access_token)

                        if user_response.user is None:
                            raise ValueError("Invalid session.")

                        columns, rows = run_student_query(sql_query)

                        st.success("Query executed successfully!")
                        st.dataframe(
                            pd.DataFrame(rows, columns=columns),
                            hide_index=True,
                        )

                    except Exception as error:
                        st.error(f"Unable to run query: {error}")

                if st.button("Save Answer", key=f"save_{question_id}"):
                    try:
                        if not sql_query.strip():
                            st.warning("Please write an SQL answer before saving.")
                        else:
                            session = st.session_state.get("auth_session")

                            if session is None:
                                raise ValueError("Please sign in.")

                            supabase = get_supabase()

                            # Establish an authenticated Supabase session.
                            auth_response = supabase.auth.set_session(
                                session.access_token,
                                session.refresh_token,
                            )

                            if auth_response.session is None:
                                raise ValueError(
                                    "Session expired. Please sign in again."
                                )

                            st.session_state["auth_session"] = auth_response.session

                            user_response = supabase.auth.get_user(
                                auth_response.session.access_token
                            )

                            if user_response.user is None:
                                raise ValueError("Invalid session.")

                            student_id = user_response.user.id

                            # Insert or update this student's answer.
                            supabase.table("quiz_submissions").upsert(
                                {
                                    "student_id": student_id,
                                    "question_id": question_id,
                                    "sql_answer": sql_query.strip(),
                                },
                                on_conflict="student_id,question_id",
                            ).execute()

                            st.success("Answer saved successfully!")

                    except Exception as error:
                        st.error(f"Unable to save answer: {error}")

    except Exception as error:
        st.error(f"Unable to load quiz questions: {error}")

else:
    st.info("Please sign in to access the SQL quiz.")
