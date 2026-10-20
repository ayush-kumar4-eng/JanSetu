"""
JanSetu Backend Configuration
Loads environment variables from backend/.env or system environment.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
ENV_PATH = BACKEND_DIR / ".env"

# Load environment variables from backend/.env if it exists
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()

# Settings
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
QDRANT_URL: str = os.getenv("QDRANT_URL", "").strip()
QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "").strip()

# SQLite Path - can be relative to backend or absolute
sqlite_raw_path = os.getenv("SQLITE_PATH", "../database/jansetu.db").strip()
if os.path.isabs(sqlite_raw_path):
    SQLITE_PATH: Path = Path(sqlite_raw_path)
else:
    SQLITE_PATH: Path = (BACKEND_DIR / sqlite_raw_path).resolve()

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

# Local vector store storage path when QDRANT_URL is not set
QDRANT_LOCAL_DIR: Path = BACKEND_DIR / "qdrant_storage"
QDRANT_LOCAL_DIR.mkdir(parents=True, exist_ok=True)

# Upload directory for demo documents
UPLOADS_DIR: Path = BACKEND_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
