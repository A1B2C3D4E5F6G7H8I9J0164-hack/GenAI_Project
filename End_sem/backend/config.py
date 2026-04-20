import os
from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
# Using Mistral 7B - excellent performance, lightweight, free tier available
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct:free")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
