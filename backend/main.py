"""
JanSetu — Agentic AI Workforce for Government Scheme Navigation
FastAPI Server Entrypoint
"""

import logging
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import HOST, PORT, SQLITE_PATH
from backend.vector_search import ensure_schemes_indexed
from backend.routers import auth, schemes, workflow, documents, applications, chat

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("JanSetu.Main")

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes vector search collection and database verification on startup."""
    logger.info("Initializing JanSetu Backend Services...")
    try:
        ensure_schemes_indexed()
        logger.info("[OK] Qdrant Scheme Semantic Index ready.")
    except Exception as e:
        logger.error(f"Error during Qdrant startup index: {e}")
    yield
    logger.info("Shutting down JanSetu services.")


app = FastAPI(
    title="JanSetu API",
    description="Agentic AI Workforce for Government Scheme Navigation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(schemes.router)
app.include_router(workflow.router)
app.include_router(documents.router)
app.include_router(applications.router)
app.include_router(applications.notifications_router)
app.include_router(chat.router)


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "JanSetu AI Workforce",
        "version": "1.0.0",
        "demo_mode": True,
        "database_connected": SQLITE_PATH.exists()
    }


# Serve Frontend Static Assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(FRONTEND_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting JanSetu server at http://{HOST}:{PORT}")
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
