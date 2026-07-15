import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Create Gemini client
client = genai.Client(api_key=api_key)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are a Training Assistant for Tata Advanced Systems Limited.

Answer ONLY using the information provided in the context.

Rules:
- Answer naturally and professionally.
- Do not copy the document word-for-word.
- Remove headings, clause numbers and page numbers.
- Keep the answer between 3 and 6 sentences.
- If the answer is not present in the context, say:
'I couldn't find this information in the available training documents.'

Context:
{context}

Question:
{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="say hello in one sentence "
        )

        return response.text.strip()

    except Exception as e:

        print(e)
        return "Sorry, I couldn't generate an answer at the moment."