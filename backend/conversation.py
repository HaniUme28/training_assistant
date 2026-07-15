from database import db
from datetime import datetime

conversation_collection = db["conversations"]
message_collection = db["messages"]


# ---------------------------------
# Create Conversation
# ---------------------------------
def create_conversation(chat_id, user_id, first_message):

    conversation = conversation_collection.find_one({
        "conversation_id": chat_id
    })

    if conversation:
        return

    title = first_message.strip()

    if len(title) > 35:
        title = title[:35] + "..."

    conversation_collection.insert_one({

        "conversation_id": chat_id,

        "user_id": user_id,

        "title": title,

        "created_at": datetime.now()

    })


# ---------------------------------
# Get Conversations
# ---------------------------------
def get_conversations(user_id):

    return list(

        conversation_collection.find(

            {
                "user_id": user_id
            },

            {
                "_id": 0
            }

        ).sort("created_at", -1)

    )


# ---------------------------------
# Delete Conversation
# ---------------------------------
def delete_conversation(chat_id):

    conversation_collection.delete_one({

        "conversation_id": chat_id

    })

    message_collection.delete_many({

        "chat_id": chat_id

    })

    return {

        "success": True,

        "message": "Conversation deleted."

    }


# ---------------------------------
# Rename Conversation
# ---------------------------------
def rename_conversation(chat_id, title):

    conversation_collection.update_one(

        {

            "conversation_id": chat_id

        },

        {

            "$set": {

                "title": title

            }

        }

    )

    return {

        "success": True

    }