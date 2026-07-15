import requests
import uuid
BASE_URL = "https://chat-assistant-nhch.onrender.com"


# -------------------------
# Login
# -------------------------
def login(email, password):
    url = f"{BASE_URL}/login"

    response = requests.post(
        url,
        json={
            "email": email,
            "password": password
        }
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        return response.json()
    except Exception:
        return {
            "success": False,
            "message": response.text
        }

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





def login(email, password):
    url = f"{BASE_URL}/login"

    response = requests.post(
        url,
        json={
            "email": email,
            "password": password
        }
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        return response.json()
    except Exception:
        return {
            "success": False,
            "message": response.text
        }