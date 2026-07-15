import streamlit as st
import uuid
import time
from datetime import datetime

from style import hide_streamlit_menu
from api import (
    chat,
    get_conversations,
    get_messages,
    delete_conversation,
    rename_conversation,
)


def chat_page():
    hide_streamlit_menu()

    # -----------------------------
    # Login Check
    # -----------------------------
    if "user" not in st.session_state:
        st.error("Please login first.")
        st.stop()

    # -----------------------------
    # Session Variables
    # -----------------------------
    if "chat_id" not in st.session_state or st.session_state.chat_id is None:
        st.session_state.chat_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -----------------------------
    # Header
    # -----------------------------
    st.title("🤖 AI Training Assistant")
    st.caption(
        "Your intelligent assistant for training materials, company policies, documents and FAQs."
    )
    st.divider()

    # ===========================================================
    # Sidebar
    # ===========================================================
    with st.sidebar:
        st.title("🤖 Training Assistant")
        st.divider()

        search = st.text_input(
            "Search Chats",
            placeholder="🔍 Search chats...",
            label_visibility="collapsed",
        )

        st.divider()

        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.chat_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()

        st.divider()
        st.subheader("💬 Recent Chats")

        conversations = get_conversations(st.session_state.user["user_id"])

        if search:
            conversations = [
                c for c in conversations if search.lower() in c["title"].lower()
            ]

        if len(conversations) == 0:
            st.caption("No conversations found.")
        else:
            for convo in conversations:
                col1, col2 = st.columns([8, 1])

                with col1:
                    if st.button(
                        f"📄 {convo['title']}",
                        key=f"chat_{convo['conversation_id']}",
                        use_container_width=True,
                    ):
                        st.session_state.chat_id = convo["conversation_id"]
                        st.session_state.messages = get_messages(
                            convo["conversation_id"]
                        )
                        st.rerun()

                with col2:
                    with st.popover("⋮"):
                        st.markdown("### Conversation")

                        new_title = st.text_input(
                            "Rename",
                            value=convo["title"],
                            key=f"title_{convo['conversation_id']}",
                        )

                        if st.button(
                            "💾 Save",
                            key=f"save_{convo['conversation_id']}",
                            use_container_width=True,
                        ):
                            rename_conversation(
                                convo["conversation_id"],
                                new_title,
                            )
                            st.rerun()

                        st.divider()

                        if st.button(
                            "🗑 Delete",
                            key=f"delete_{convo['conversation_id']}",
                            use_container_width=True,
                        ):
                            delete_conversation(convo["conversation_id"])
                            st.session_state.chat_id = str(uuid.uuid4())
                            st.session_state.messages = []
                            st.rerun()

        st.divider()
        st.write(f"👤 **{st.session_state.user['name']}**")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        st.divider()
        st.caption("AI Training Assistant v1.0")

    # ===========================================================
    # Welcome Screen
    # ===========================================================
    if len(st.session_state.messages) == 0:
        st.markdown(f"## Welcome, {st.session_state.user['name']} 👋")
        st.info(
            """
You can ask me about:

• Company Policies

• HR Guidelines

• Leave Rules

• Employee Benefits

• Attendance

• Safety Procedures

• Training Material
"""
        )

    # ===========================================================
    # Display Messages
    # ===========================================================
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if "time" in message:
                st.caption(message["time"])

    # ===========================================================
    # Chat Input
    # ===========================================================
    question = st.chat_input("Message AI Training Assistant...")

    if question:
        user_time = datetime.now().strftime("%I:%M %p")

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
                "time": user_time,
            }
        )

        with st.chat_message("user", avatar="👤"):
            st.markdown(question)
            st.caption(user_time)

        # -----------------------------
        # Bot Response
        # -----------------------------
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()

            for text in [
                "🤖 Thinking.",
                "🤖 Thinking..",
                "🤖 Searching documents...",
            ]:
                placeholder.markdown(text)
                time.sleep(0.3)

            response = chat(
                question,
                st.session_state.user["user_id"],
                st.session_state.chat_id,
            )

            # -----------------------------
            # Process Response
            # -----------------------------
            if "answer" in response:
                answer = response["answer"]
                pdf = response.get("pdf")
                link = response.get("link")
            else:
                answer = "⚠️ Backend Error:\n\n" + str(response)
                pdf = None
                link = None

            placeholder.markdown(answer)

            # -----------------------------
            # Show PDF if available
            # -----------------------------
            if pdf:
                pdf_url = f"http://127.0.0.1:8000/documents/{pdf}"
                st.markdown("### 📄 Related Document")
                st.link_button(
                    "📄 Download PDF",
                    pdf_url,
                    use_container_width=True,
                )

            # -----------------------------
            # Show Link if available
            # -----------------------------
            if link:
                st.markdown("### 🌐 Related Link")
                st.markdown(f"🔗 [Open Website]({link})")

            # -----------------------------
            # Timestamp
            # -----------------------------
            bot_time = datetime.now().strftime("%I:%M %p")
            st.caption(bot_time)

        # -----------------------------
        # Save Chat History
        # -----------------------------
        bot_message = answer

        if pdf:
            bot_message += f"\n\n📄 PDF: {pdf}"

        if link:
            bot_message += f"\n\n🔗 {link}"

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_message,
                "time": bot_time,
            }
        )