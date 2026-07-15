import requests
import uuid
BASE_URL = "http://127.0.0.1:8000"


# -------------------------
# Login
# -------------------------
def login(email, password):

    response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": email,
            "password": password
        }
    )

    return response.json()


# -------------------------
# Signup
# -------------------------
def signup(name, email, password):

    response = requests.post(
        f"{BASE_URL}/signup",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )

    return response.json()


# -------------------------
# Chat
# -------------------------
# -------------------------
# Chat
# -------------------------
def chat(question, user_id, chat_id):

    if not chat_id:

        chat_id = str(uuid.uuid4())


    payload = {

        "question": question,

        "user_id": user_id,

        "chat_id": chat_id

    }


    print("CHAT REQUEST SENT:")
    print(payload)


    response = requests.post(

        f"{BASE_URL}/chat",

        json=payload

    )


    print("CHAT RESPONSE:")
    print(response.json())


    return response.json()


   


# -------------------------
# Get Conversations
# -------------------------
def get_conversations(user_id):

    response = requests.get(
        f"{BASE_URL}/conversations/{user_id}"
    )

    return response.json()


# -------------------------
# Get Messages
# -------------------------
def get_messages(chat_id):

    response = requests.get(
        f"{BASE_URL}/messages/{chat_id}"
    )

    return response.json()


# -------------------------
# Delete Conversation
# -------------------------
def delete_conversation(chat_id):

    response = requests.delete(
        f"{BASE_URL}/conversation/{chat_id}"
    )

    return response.json()


# -------------------------
# Rename Conversation
# -------------------------
def rename_conversation(chat_id, title):

    response = requests.put(
        f"{BASE_URL}/conversation/{chat_id}",
        json={
            "title": title
        }
    )

    return response.json()