from semantic_search import get_best_answer

def search_pdf(user_question):
    """
    Lightweight fallback using MongoDB semantic search.
    """

    print(f"Processing query: {user_question}")

    match = get_best_answer(user_question)

    if match:
        return {
            "answer": match["answer"],
            "pdf": match.get("pdf"),
            "link": match.get("link")
        }

    return None