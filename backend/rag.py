from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

import os
import re


# ----------------------------
# Clean PDF text
# ----------------------------

def clean_text(text):

    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text)

    text = re.sub(r"\n\d+\.\s*", "\n", text)

    text = re.sub(
        r"ANNEXURE.*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"Revision.*",
        "",
        text
    )

    text = re.sub(
        r"\n{2,}",
        "\n",
        text
    )

    return text.strip()



# ----------------------------
# PDF Folder
# ----------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PDF_FOLDER = os.path.join(
    BASE_DIR,
    "..",
    "documents"
)



# ----------------------------
# Load PDFs
# ----------------------------

loader = PyPDFDirectoryLoader(
    PDF_FOLDER
)

documents = loader.load()


print(
    f"Loaded {len(documents)} PDF pages"
)



# ----------------------------
# Create Vector Database
# ----------------------------

if len(documents) == 0:

    retriever = None


else:


    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=250
    )


    docs = splitter.split_documents(
        documents
    )


    for doc in docs:

        doc.page_content = clean_text(
            doc.page_content
        )


    print(
        f"Created {len(docs)} chunks"
    )



    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/all-MiniLM-L6-v2"

    )


    vectorstore = FAISS.from_documents(

        docs,

        embeddings

    )


    print(
        "FAISS Vector Database Created Successfully!"
    )


    retriever = vectorstore.as_retriever(
    search_kwargs={"k": 1}
)



# ----------------------------
# PDF Search
# ----------------------------

# ----------------------------
# PDF Search
# ----------------------------

def search_pdf(question):

    if retriever is None:
        return None

    # Get document with similarity score
    results = vectorstore.similarity_search_with_score(
        question,
        k=1
    )

    if not results:
        return None

    best_result, score = results[0]

    print("PDF Similarity Score:", score)

    # Reject poor matches
    if score > 1.0:
        return None

    pdf_name = None

    if "source" in best_result.metadata:
        pdf_name = os.path.basename(
            best_result.metadata["source"]
        )

    return {

        "answer": best_result.page_content.strip(),

        "pdf": pdf_name,

        "link": None

    }