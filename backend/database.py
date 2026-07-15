from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

print("MONGO_URL:", MONGO_URL)

client = MongoClient(MONGO_URL)

db = client["CollegeChatbot"]

print("Database Name:", db.name)
print("Collections:", db.list_collection_names())

users_collection = db["users"]
faq_collection = db["faqs"]
conversation_collection = db["conversations"]
message_collection = db["messages"]