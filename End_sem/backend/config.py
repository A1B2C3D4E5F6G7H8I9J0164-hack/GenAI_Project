import os
from dotenv import load_dotenv

# Load .env from project root (parent of backend/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
# Upgraded to better free NVIDIA model with superior instruction following
MODEL_NAME = os.getenv("MODEL_NAME", "nvidia/llama-3.1-nemotron-70b-instruct:free")
EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
