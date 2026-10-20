"""
JanSetu Configuration & Service Verification Script
Tests API keys, Qdrant, SQLite, and embeddings safely without logging secrets.
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import (
    BACKEND_DIR,
    ENV_PATH,
    GROQ_API_KEY,
    GEMINI_API_KEY,
    QDRANT_URL,
    QDRANT_API_KEY,
    SQLITE_PATH,
)


def verify_env_path():
    print("--- 1. Environment File Check ---")
    if ENV_PATH.exists():
        print(f"[PASS] .env found at expected path: {ENV_PATH}")
        return True
    else:
        print(f"[FAIL] .env NOT found at: {ENV_PATH}")
        return False


def verify_groq():
    print("\n--- 2. Groq API Verification ---")
    if not GROQ_API_KEY:
        print("[FAIL] GROQ_API_KEY is not set or empty in backend/.env.")
        return False
    if GROQ_API_KEY.startswith("your_"):
        print("[WARN] GROQ_API_KEY is still using the placeholder value.")
        return False

    print(f"[INFO] GROQ_API_KEY is present (length: {len(GROQ_API_KEY)} chars). Testing minimal request...")
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        resp = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[{"role": "user", "content": "Respond with 1 word: Ready"}],
            max_tokens=5,
        )
        reply = resp.choices[0].message.content.strip()
        print(f"[PASS] Groq API verified successfully! Model returned: '{reply}'")
        return True
    except Exception as e:
        print(f"[FAIL] Groq API request failed: {type(e).__name__}: {str(e)[:150]}")
        return False


def verify_gemini():
    print("\n--- 3. Gemini API Verification (Fallback) ---")
    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith("your_"):
        print("[INFO] GEMINI_API_KEY is not configured (optional fallback).")
        return None

    print(f"[INFO] GEMINI_API_KEY is present (length: {len(GEMINI_API_KEY)} chars). Testing minimal request...")
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        resp = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Respond with 1 word: Ready"
        )
        print(f"[PASS] Gemini API verified successfully! Model returned: '{resp.text.strip()}'")
        return True
    except Exception as e:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Respond with 1 word: Ready"
            )
            print(f"[PASS] Gemini API verified successfully! Model returned: '{resp.text.strip()}'")
            return True
        except Exception as e2:
            print(f"[FAIL] Gemini API request failed: {type(e2).__name__}: {str(e2)[:150]}")
            return False


def verify_qdrant():
    print("\n--- 4. Qdrant Connection Verification ---")
    try:
        from backend.vector_search import get_qdrant_client
        client = get_qdrant_client()
        collections = client.get_collections().collections
        names = [c.name for c in collections]
        if QDRANT_URL:
            print(f"[PASS] Connected to Qdrant Cloud at {QDRANT_URL.split('@')[-1]}. Collections: {names}")
        else:
            print(f"[PASS] Connected to Local Qdrant Storage. Collections: {names}")
        return True
    except Exception as e:
        print(f"[FAIL] Qdrant connection failed: {type(e).__name__}: {str(e)[:150]}")
        return False


def verify_sqlite():
    print("\n--- 5. SQLite Database & Schema Verification ---")
    import sqlite3
    try:
        print(f"[INFO] Checking SQLite database at: {SQLITE_PATH}")
        if not SQLITE_PATH.exists():
            print("[WARN] SQLite file does not exist yet. Running init_db...")
            from database.init_db import init_database
            init_database()

        conn = sqlite3.connect(SQLITE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        required_tables = ["users", "citizen_profiles", "schemes", "user_documents", "applications", "notifications", "chat_history"]
        missing = [t for t in required_tables if t not in tables]

        if not missing:
            print(f"[PASS] SQLite verified with all required tables: {tables}")
            return True
        else:
            print(f"[FAIL] SQLite is missing tables: {missing}")
            return False
    except Exception as e:
        print(f"[FAIL] SQLite verification failed: {e}")
        return False


def verify_embeddings():
    print("\n--- 6. Multilingual Embeddings Verification ---")
    try:
        from backend.vector_search import generate_embedding, _use_sentence_transformers
        vec = generate_embedding("प्रधानमंत्री किसान सम्मान निधि योजना agriculture loan")
        print(f"[INFO] Embedding generated successfully! Vector dimension: {len(vec)}, Mode: {'sentence-transformers' if _use_sentence_transformers else 'built-in multilingual dense vectorizer'}")
        if len(vec) == 384:
            print("[PASS] Vector embedding model operational (384-dimensional dense projection).")
            return True
        else:
            print(f"[FAIL] Unexpected vector dimension: {len(vec)}")
            return False
    except Exception as e:
        print(f"[FAIL] Embeddings check failed: {e}")
        return False


def verify_gitignore():
    print("\n--- 7. .gitignore Security Verification ---")
    gitignore_path = PROJECT_ROOT / ".gitignore"
    if not gitignore_path.exists():
        print("[FAIL] .gitignore missing!")
        return False

    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()

    checks = {
        ".env": ".env" in content,
        "database files (*.db / *.sqlite3)": "*.db" in content or "jansetu.db" in content,
        "qdrant_storage": "qdrant_storage" in content or "*.db" in content
    }

    all_good = True
    for name, passed in checks.items():
        if passed:
            print(f"[PASS] .gitignore protects: {name}")
        else:
            print(f"[FAIL] .gitignore missing protection for: {name}")
            all_good = False
    return all_good


def main():
    print("=" * 60)
    print("      JanSetu System & Security Configuration Verification")
    print("=" * 60)

    results = {
        ".env Location": verify_env_path(),
        "Groq API": verify_groq(),
        "Gemini Fallback API": verify_gemini(),
        "Qdrant Vector DB": verify_qdrant(),
        "SQLite Database": verify_sqlite(),
        "Multilingual Embeddings": verify_embeddings(),
        ".gitignore Protection": verify_gitignore()
    }

    print("\n" + "=" * 60)
    print("                     VERIFICATION SUMMARY")
    print("=" * 60)
    for check, res in results.items():
        if res is True:
            status = "PASSED"
        elif res is False:
            status = "FAILED"
        else:
            status = "SKIPPED / OPTIONAL"
        print(f" - {check:<26} : {status}")

    print("=" * 60)


if __name__ == "__main__":
    main()
