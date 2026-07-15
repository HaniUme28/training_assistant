import streamlit as st


def hide_streamlit_menu():

    st.markdown(
        """
        <style>

        /* Hide Deploy button */
        [data-testid="stAppDeployButton"] {
            display: none;
        }


        /* Hide Rerun */
        [data-testid="stToolbar"] button:nth-child(1) {
            display:none;
        }


        /* Hide extra menu items */
        .stDeployButton {
            display:none;
        }


        </style>
        """,
        unsafe_allow_html=True
    )