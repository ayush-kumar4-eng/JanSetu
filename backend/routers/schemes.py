"""
JanSetu Welfare Schemes Routes
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from backend.db import get_all_schemes, get_scheme_by_id, get_scheme_by_code
from backend.vector_search import search_schemes

router = APIRouter(prefix="/api/schemes", tags=["Schemes"])


@router.get("")
def list_schemes(category: Optional[str] = Query(None, description="Filter by category")):
    """Returns schemes list, optionally filtered by category."""
    schemes = get_all_schemes(category=category)
    return {"count": len(schemes), "schemes": schemes}


@router.get("/categories")
def list_categories():
    """Returns unique list of scheme categories."""
    schemes = get_all_schemes()
    categories = sorted(list(set(s["category"] for s in schemes if s.get("category"))))
    return {"categories": categories}


@router.get("/search")
def search_scheme_catalog(
    q: str = Query(..., description="Semantic search query in plain language"),
    category: Optional[str] = Query(None, description="Optional category filter"),
    limit: int = Query(6, ge=1, le=20)
):
    """Semantic vector search against Qdrant index."""
    results = search_schemes(q, limit=limit, category=category)
    return {"query": q, "count": len(results), "results": results}


@router.get("/{scheme_id}")
def get_scheme(scheme_id: int):
    """Retrieves full details for a scheme."""
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return {"scheme": scheme}
