from database import message_collection
# ----------------------------------
# Save One Message
# ----------------------------------
def save_message(chat_id, role, content):

    message_collection.insert_one({

        "chat_id": chat_id,
        "role": role,
        "content": content

    })


# ----------------------------------
# Get Previous Messages
# ----------------------------------
def get_recent_memory(chat_id, limit=10):

    messages = list(

        message_collection.find(
            {
                "chat_id": chat_id
            }
        ).sort("_id", 1).limit(limit)

    )

    return messages


# ----------------------------------
# Get All Messages of One Conversation
# ----------------------------------
def get_messages(chat_id):

    messages = list(

        message_collection.find(

            {
                "chat_id": chat_id
            },

            {
                "_id": 0
            }

        ).sort("_id", 1)

    )

    return messages