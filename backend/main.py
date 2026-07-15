from fastapi import FastAPI
from pydantic import BaseModel


from auth import create_user, login_user

from conversation import (
    create_conversation,
    get_conversations,
    delete_conversation,
    rename_conversation
)

from semantic_search import get_best_answer
from rag import search_pdf

from memory import (
    save_message,
    get_recent_memory,
    get_messages
)
from pathlib import Path
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR.parent / "documents"

print("Documents folder:", DOCUMENTS_DIR)
print("Exists:", DOCUMENTS_DIR.exists())

app.mount(
    "/documents",
    StaticFiles(directory=str(DOCUMENTS_DIR)),
    name="documents"
)




# ----------------------------------
# Models
# ----------------------------------

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str



class LoginRequest(BaseModel):
    email: str
    password: str



class ChatRequest(BaseModel):
    question: str
    user_id: str
    chat_id: str



class RenameRequest(BaseModel):
    title: str



class ChatResponse(BaseModel):
    answer: str
    pdf: str | None = None
    link: str | None = None




# ----------------------------------
# Signup
# ----------------------------------

@app.post("/signup")
def signup(request: SignupRequest):

    print("========= SIGNUP REQUEST ==========")
    print("Name:", request.name)
    print("Email:", request.email)


    return create_user(
        request.name,
        request.email,
        request.password
    )




# ----------------------------------
# Login
# ----------------------------------

@app.post("/login")
def login(request: LoginRequest):

    return login_user(
        request.email,
        request.password
    )





# ----------------------------------
# Chat
# ----------------------------------

# ----------------------------------
# Chat
# ----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # -----------------------------
    # Create Conversation
    # -----------------------------
    create_conversation(
        request.chat_id,
        request.user_id,
        request.question
    )

    # -----------------------------
    # Save User Message
    # -----------------------------
    save_message(
        request.chat_id,
        "user",
        request.question
    )

    answer = None
    pdf = None
    link = None

    question = request.question.lower().strip()

    # -----------------------------
    # Greetings
    # -----------------------------
    greetings = [
        "hi",
        "hello",
        "hey",
        "heyy",
        "hii",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    goodbye = [
        "bye",
        "goodbye",
        "see you"
    ]

    if question in greetings:

        answer = (
            "Hello! 👋\n\n"
            "I'm your AI Training Assistant. "
            "How can I help you today?"
        )

    elif question in goodbye:

        answer = (
            "Goodbye! 👋\n"
            "Have a wonderful day."
        )

    # -----------------------------
    # FAQ Search
    # -----------------------------
    if answer is None:

        faq_result = get_best_answer(request.question)

        if faq_result:

            answer = faq_result["answer"]
            pdf = faq_result.get("pdf")
            link = faq_result.get("link")

    # -----------------------------
    # PDF Search
    # -----------------------------
    if answer is None:

        pdf_result = search_pdf(request.question)

        if pdf_result:

            answer = pdf_result["answer"]
            pdf = pdf_result.get("pdf")
            link = pdf_result.get("link")

    # -----------------------------
    # No Answer
    # -----------------------------
    if answer is None:

        answer = (
            "Sorry, I couldn't find any relevant information "
            "for your question."
        )

    # -----------------------------
    # Save Assistant Message
    # -----------------------------
    save_message(
        request.chat_id,
        "assistant",
        answer
    )

    # -----------------------------
    # Return Response
    # -----------------------------
    return {

        "answer": answer,

        "pdf": pdf,

        "link": link

    }

# ----------------------------------
# Get Conversation List
# ----------------------------------

@app.get("/conversations/{user_id}")
def conversations(user_id: str):

    return get_conversations(user_id)





# ----------------------------------
# Get Messages
# ----------------------------------

@app.get("/messages/{chat_id}")
def messages(chat_id: str):

    return get_messages(chat_id)





# ----------------------------------
# Delete Conversation
# ----------------------------------

@app.delete("/conversation/{chat_id}")
def delete(chat_id: str):

    return delete_conversation(chat_id)





# ----------------------------------
# Rename Conversation
# ----------------------------------

@app.put("/conversation/{chat_id}")
def rename(
    chat_id: str,
    request: RenameRequest
):

    return rename_conversation(

        chat_id,

        request.title

    )