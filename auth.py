import os

import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Missing Supabase configuration")

    return create_client(url, key)


def show_auth():
    st.subheader("Student Account")

    if "auth_session" not in st.session_state:
        st.session_state.auth_session = None

    if st.session_state.auth_session:
        st.success("You are signed in!")

        if st.button("Sign Out"):
            st.session_state.auth_session = None
            st.rerun()

        return

    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    with tab1:
        with st.form("signin_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In")

        if submitted:
            try:
                supabase = get_supabase()
                response = supabase.auth.sign_in_with_password(
                    {
                        "email": email,
                        "password": password,
                    }
                )
                st.session_state.auth_session = response.session
                st.rerun()
            except Exception as error:
                st.error(f"Sign-in failed: {error}")

    with tab2:
        with st.form("signup_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            registered = st.form_submit_button("Create Account")

        if registered:
            try:
                supabase = get_supabase()
                supabase.auth.sign_up(
                    {
                        "email": new_email,
                        "password": new_password,
                    }
                )
                st.success("Account created successfully! You can now sign in.")
            except Exception as error:
                st.error(f"Registration failed: {error}")
