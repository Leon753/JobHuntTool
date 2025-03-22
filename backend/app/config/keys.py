import os
from dotenv import load_dotenv

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = os.getenv("PERPLEXITY_API_URL")
OPENAI_GPT4_KEY = os.getenv("AZURE_API_KEY")
ENDPOINT_OPENAI_GPT4 = os.getenv("AZURE_API_BASE")
TEXT_EMBEDDINGS_API_KEY = os.getenv("TEXT_EMBEDDINGS_API_KEY")
TEXT_EMBEDDINGS_API_BASE = os.getenv("TEXT_EMBEDDINGS_API_BASE")
TEXT_EMBEDDINGS_API_VERSION = os.getenv("TEXT_EMBEDDINGS_API_VERSION")
CHAT_VERSION = "2024-08-01-preview"  # Update if needed
CHAT_DEPLOYMENT_NAME = "gpt-4o"  # Replace with your deployed model name

