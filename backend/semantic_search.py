import re

# ---------------------------------------
# Lightweight Token Matcher (Uses 0MB RAM)
# ---------------------------------------
def get_tokens(text):
    """Converts string into lowercase word tokens."""
    return set(re.findall(r'\w+', text.lower()))

def calculate_similarity(str1, str2):
    """Calculates Jaccard Similarity coefficient between two strings."""
    tokens1 = get_tokens(str1)
    tokens2 = get_tokens(str2)
    
    if not tokens1 or not tokens2:
        return 0.0
        
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    return float(len(intersection)) / len(union)

# ---------------------------------------
# Semantic Search (Render Free Optimized)
# ---------------------------------------
def get_best_answer(user_question):
    # Dynamic import so database config is only queried when called
    from database import db
    
    faq_collection = db["faqs"]
    faqs = list(faq_collection.find())

    if not faqs:
        return None

    best_score = -1.0
    best_faq = None
    best_match_text = ""

    # Check match score for each FAQ question row
    for faq in faqs:
        score = calculate_similarity(user_question, faq["question"])
        if score > best_score:
            best_score = score
            best_faq = faq
            best_match_text = faq["question"]

    print(f"Best Match: {best_match_text}")
    print(f"Similarity Score: {best_score:.3f}")

    # Adjusted threshold for token overlap matching
    if best_score >= 0.35:
        pdf = best_faq.get("pdf")
        link = best_faq.get("link")

        return {
            "answer": best_faq["answer"],
            "pdf": pdf,
            "link": link
        }

    return None