import streamlit as st

from login import login_page
from signup import signup_page
from chat import chat_page

st.set_page_config(
    page_title="🤖 AI Training Assistant",
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.logged_in:

    chat_page()

else:

    if st.session_state.page == "login":

        login_page()

        st.write("Don't have an account?")

        if st.button("Create Account"):

            st.session_state.page = "signup"
            st.rerun()

    else:

        signup_page()

        st.write("Already have an account?")

        if st.button("Login"):

            st.session_state.page = "login"
            st.rerun()