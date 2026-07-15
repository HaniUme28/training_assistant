import streamlit as st
from api import (
    login,
    get_conversations,
    get_messages
)
from style import hide_streamlit_menu


def login_page():
    hide_streamlit_menu()

    st.title("🤖 AI Training Assistant")

    st.subheader("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        result = login(email, password)

        if result["success"]:

            # -------------------------
            # Login Status
            # -------------------------
            st.session_state.logged_in = True

            # -------------------------
            # Store User Information
            # -------------------------
            st.session_state.user = {

                "user_id": result["user_id"],

                "name": result["name"],

                "email": result["email"]

            }

            # -------------------------
            # Load Previous Conversations
            # -------------------------
            conversations = get_conversations(
                result["user_id"]
            )

            if len(conversations) > 0:

                latest = conversations[0]

                st.session_state.chat_id = latest["conversation_id"]

                st.session_state.messages = get_messages(
                    latest["conversation_id"]
                )

            else:

                st.session_state.chat_id = None

                st.session_state.messages = []

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error(result["message"])