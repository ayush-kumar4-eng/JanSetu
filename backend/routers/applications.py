"""
JanSetu Applications & Tracking Routes
"""

from fastapi import APIRouter, HTTPException
from backend.db import (
    get_user_applications,
    get_application_by_ref,
    get_user_notifications,
    get_user_by_id
)

router = APIRouter(prefix="/api/applications", tags=["Applications & Tracking"])


@router.get("/user/{user_id}")
def list_user_applications(user_id: int):
    """Returns all applications submitted by the citizen."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    apps = get_user_applications(user_id)
    return {"user_id": user_id, "count": len(apps), "applications": apps}


@router.get("/ref/{reference_no}")
def get_application_details(reference_no: str):
    """Retrieves full application details and simulated tracking timeline by reference number."""
    app = get_application_by_ref(reference_no)
    if not app:
        raise HTTPException(status_code=404, detail=f"Application with Ref {reference_no} not found")
    return {"application": app}


@router.get("/notifications/user/{user_id}")
def list_notifications(user_id: int):
    """Returns simulated notification feed for the citizen."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    notifs = get_user_notifications(user_id)
    return {"user_id": user_id, "count": len(notifs), "notifications": notifs}


notifications_router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


@notifications_router.get("/user/{user_id}")
def list_user_notifications_direct(user_id: int):
    """Returns simulated notification feed for the citizen directly under /api/notifications."""
    return list_notifications(user_id)
