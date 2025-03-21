from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import os

# Constants
DB_PATH = "faiss_test_db"
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create a dummy document
doc = Document(page_content="test message", metadata={"source": "test"})

# Create and save FAISS
print("Creating FAISS DB...")
db = FAISS.from_documents([doc], embedding_model)
db.save_local(DB_PATH)

# Check if files were created
print("Created files:", os.listdir(DB_PATH))
