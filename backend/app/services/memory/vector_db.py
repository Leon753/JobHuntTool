import os
from pathlib import Path
from langchain_chroma import Chroma  # Using the dedicated chroma package
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

SIMILARITY_THRESHOLD = 0.80
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
PERSIST_DIRECTORY = "chroma_messages_db"
COLLECTION_NAME = "messages"

def create_vector_db():
    # Check if the persist directory exists and is non-empty.
    if not os.path.exists(PERSIST_DIRECTORY) or not os.listdir(PERSIST_DIRECTORY):
        print("Creating Chroma DB (empty collection)...")
        # Creating a new Chroma collection (this will create the collection on disk)
        db = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=EMBEDDING_MODEL,  # Pass the entire embedding object
            collection_name=COLLECTION_NAME
        )
        print("Chroma DB created.")
    else:
        print("Chroma DB already exists.")

def add_message(query: str, result):
    print("ADD MESSAGE:", query)
    new_doc = Document(page_content=query, metadata={"answer": result})
    # Load the persistent collection using the constructor.
    db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=EMBEDDING_MODEL,
        collection_name=COLLECTION_NAME
    )
    db.add_documents([new_doc])
    print("Added message to Chroma DB.")

def similarity_search(query):
    try:
        print("SIMILARITY SEARCH")
        print("QUERY:", query)
        db = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=EMBEDDING_MODEL,
            collection_name=COLLECTION_NAME
        )
        results = db.similarity_search_with_score(query, k=2)
        strict_results = []
        for doc, score in results:
            # Here we assume score is a distance (0 for exact match) so we convert: similarity = 1 - score.
            similarity = 1 - score
            print(f"Found: {doc.page_content} | similarity: {similarity:.3f}")
            if similarity >= SIMILARITY_THRESHOLD:
                strict_results.append((doc, similarity))
        if len(strict_results) != 1:
            print("NO RESULTS FOUND")
            return None
        else:
            print("SIMILAR:", strict_results[0][0].metadata)
            return strict_results[0][0].metadata
    except Exception as e:
        print("ERROR IN SIMILARITY SEARCH:", e)
        return None

"""
# --- End-to-End Flow Example ---
create_vector_db()
add_message("what is the capital of France?", {"answer": "Paris"})
result = similarity_search("what is the capital of France?")
print("RESULT:", result)
"""
