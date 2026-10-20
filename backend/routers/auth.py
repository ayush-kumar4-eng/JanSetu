"""
JanSetu User & Citizen Profile Routes
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.db import (
    get_all_users,
    get_user_by_id,
    get_user_by_username_or_email,
    create_citizen_user,
    update_citizen_profile
)

router = APIRouter(prefix="/api/users", tags=["Users & Profiles"])


class LoginRequest(BaseModel):
    identifier: str


class RegisterRequest(BaseModel):
    username: str
    full_name: str
    email: str
    phone: Optional[str] = ""
    state: Optional[str] = "Rajasthan"
    district: Optional[str] = "Jaipur"
    age: Optional[int] = 30
    gender: Optional[str] = "Male"
    occupation: Optional[str] = "Citizen"
    annual_income: Optional[float] = 120000.0
    social_category: Optional[str] = "General"
    residence_area: Optional[str] = "Urban"
    land_ownership_hectares: Optional[float] = 0.0
    is_bpl: Optional[bool] = False


class DemoSessionRequest(BaseModel):
    persona: str = "ramesh_farmer"  # ramesh_farmer, sunita_artisan, priya_student


class ProfileUpdateRequest(BaseModel):
    age: Optional[int] = 35
    gender: Optional[str] = "Male"
    occupation: Optional[str] = "Worker"
    annual_income: Optional[float] = 120000.0
    social_category: Optional[str] = "OBC"
    marital_status: Optional[str] = "Married"
    is_differently_abled: Optional[bool] = False
    land_ownership_hectares: Optional[float] = 0.0
    residence_area: Optional[str] = "Urban"
    family_members_count: Optional[int] = 4
    is_bpl: Optional[bool] = False
    raw_attributes: Optional[Dict[str, Any]] = {}


@router.post("/login")
def login(req: LoginRequest):
    """Logs in an existing citizen or demo persona."""
    user = get_user_by_username_or_email(req.identifier)
    if not user:
        # Check if they sent an integer user_id
        if req.identifier.strip().isdigit():
            user = get_user_by_id(int(req.identifier.strip()))
    if not user:
        raise HTTPException(status_code=404, detail="Citizen profile not found. Please register or select a Demo persona.")
    return {
        "status": "authenticated",
        "demo_mode": True,
        "token": f"demo-token-{user['id']}",
        "user": user
    }


@router.post("/register")
def register(req: RegisterRequest):
    """Registers a new citizen with demographic attributes."""
    existing = get_user_by_username_or_email(req.username) or get_user_by_username_or_email(req.email)
    if existing:
        return {
            "status": "authenticated",
            "message": "Citizen already registered, logged in directly.",
            "demo_mode": True,
            "token": f"demo-token-{existing['id']}",
            "user": existing
        }

    profile_data = {
        "age": req.age,
        "gender": req.gender,
        "occupation": req.occupation,
        "annual_income": req.annual_income,
        "social_category": req.social_category,
        "residence_area": req.residence_area,
        "land_ownership_hectares": req.land_ownership_hectares,
        "is_bpl": req.is_bpl
    }
    new_user = create_citizen_user(
        username=req.username,
        full_name=req.full_name,
        email=req.email,
        phone=req.phone or "",
        state=req.state or "Rajasthan",
        district=req.district or "Jaipur",
        profile_data=profile_data
    )
    return {
        "status": "authenticated",
        "message": "Citizen registered successfully.",
        "demo_mode": True,
        "token": f"demo-token-{new_user['id']}",
        "user": new_user
    }


@router.post("/demo-session")
def demo_session(req: DemoSessionRequest):
    """Instantly switches to a verified demo citizen persona."""
    all_users = get_all_users()
    target_user = None
    for u in all_users:
        if req.persona.lower() in u.get("username", "").lower():
            target_user = u
            break
    if not target_user and all_users:
        target_user = all_users[0]

    if not target_user:
        raise HTTPException(status_code=404, detail="No demo personas found.")

    return {
        "status": "authenticated",
        "demo_mode": True,
        "token": f"demo-token-{target_user['id']}",
        "user": target_user
    }


@router.get("")
def list_users():
    """Returns all demo citizen personas."""
    return {"users": get_all_users()}


@router.get("/{user_id}")
def get_user(user_id: int):
    """Fetches details for a specific user and citizen profile."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}


@router.put("/{user_id}/profile")
def update_profile(user_id: int, req: ProfileUpdateRequest):
    """Updates the citizen profile."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile_dict = req.model_dump()
    update_citizen_profile(user_id, profile_dict)
    updated = get_user_by_id(user_id)
    return {"message": "Profile updated successfully", "user": updated}
