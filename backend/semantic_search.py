from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from database import db

# ---------------------------------------
# Load model once
# ---------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------
# Semantic Search
# ---------------------------------------

def get_best_answer(user_question):

    faq_collection = db["faqs"]

    faqs = list(faq_collection.find())

    if not faqs:
        return None

    # ---------------------------------------
    # FAQ Questions
    # ---------------------------------------

    questions = []

    for faq in faqs:
        questions.append(faq["question"])

    # ---------------------------------------
    # Embeddings
    # ---------------------------------------

    faq_embeddings = model.encode(
        questions,
        convert_to_numpy=True
    )

    user_embedding = model.encode(
        [user_question],
        convert_to_numpy=True
    )

    # ---------------------------------------
    # Similarity
    # ---------------------------------------

    similarities = cosine_similarity(
        user_embedding,
        faq_embeddings
    )[0]

    best_index = similarities.argmax()

    best_score = similarities[best_index]

    print(
        f"Best Match: {questions[best_index]}"
    )

    print(
        f"Similarity Score: {best_score:.3f}"
    )

    # ---------------------------------------
    # Lower Threshold
    # ---------------------------------------

    if best_score >= 0.55:

        best_faq = faqs[best_index]

        pdf = best_faq.get("pdf")
        link = best_faq.get("link")

        return {

            "answer": best_faq["answer"],

            "pdf": pdf,

            "link": link

        }

    return None