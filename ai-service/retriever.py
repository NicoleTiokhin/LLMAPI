import os

KNOWLEDGE_PATH = "knowledge_base"


def load_documents():
    documents = []

    for filename in os.listdir(KNOWLEDGE_PATH):
        filepath = os.path.join(KNOWLEDGE_PATH, filename)

        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                documents.append(f.read())

    return documents


def retrieve_relevant_content(answer: str) -> str:
    documents = load_documents()

    if not documents:
        return ""

    answer_words = answer.lower().split()
    matched_docs = []

    for doc in documents:
        doc_lower = doc.lower()
        if any(word in doc_lower for word in answer_words):
            matched_docs.append(doc)

    if matched_docs:
        return "\n\n".join(matched_docs[:2])

    return documents[0]