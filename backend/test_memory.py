from memory import get_chat_history

history = get_chat_history()

print("\nRecent Conversations:\n")

for chat in history:
    print("User:", chat["question"])
    print("Bot :", chat["answer"])
    print("-" * 50)