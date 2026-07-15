import streamlit as st
from api import signup


def signup_page():

    st.title("🤖 AI Training Assistant")

    st.subheader("Create Account")

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Create Account", use_container_width=True):

        # Validation
        if name.strip() == "":
            st.error("Please enter your name.")
            return

        if email.strip() == "":
            st.error("Please enter your email.")
            return

        if password.strip() == "":
            st.error("Please enter your password.")
            return

        # Call Backend
        result = signup(
            name,
            email,
            password
        )

        

        if result.get("success"):

            st.success(result["message"])

            st.info("Account created successfully. Please login.")

            st.session_state.page = "login"

            st.rerun()

        else:

            st.error(result.get("message", "Signup failed."))