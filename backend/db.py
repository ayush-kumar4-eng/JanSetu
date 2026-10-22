"""
JanSetu Database Manager and Operations
Handles SQLite queries, schemas, and CRUD operations.
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.config import SQLITE_PATH


def get_db_connection() -> sqlite3.Connection:
    """Creates a database connection with dict-like row access."""
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# ==========================================
# User and Citizen Profile CRUD
# ==========================================

def get_all_users() -> List[Dict[str, Any]]:
    """Returns all registered users with their profiles."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.username, u.full_name, u.email, u.phone, u.state, u.district,
                   p.age, p.gender, p.occupation, p.annual_income, p.social_category,
                   p.marital_status, p.is_differently_abled, p.land_ownership_hectares,
                   p.residence_area, p.family_members_count, p.is_bpl, p.raw_attributes_json
            FROM users u
            LEFT JOIN citizen_profiles p ON u.id = p.user_id
            ORDER BY u.id ASC
        """)
        rows = cursor.fetchall()
        result = []
        for r in rows:
            user_dict = dict(r)
            if user_dict.get("raw_attributes_json"):
                try:
                    user_dict["raw_attributes"] = json.loads(user_dict["raw_attributes_json"])
                except Exception:
                    user_dict["raw_attributes"] = {}
            result.append(user_dict)
        return result


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single user along with their citizen profile."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.username, u.full_name, u.email, u.phone, u.state, u.district,
                   p.id as profile_id, p.age, p.gender, p.occupation, p.annual_income,
                   p.social_category, p.marital_status, p.is_differently_abled,
                   p.land_ownership_hectares, p.residence_area, p.family_members_count,
                   p.is_bpl, p.raw_attributes_json
            FROM users u
            LEFT JOIN citizen_profiles p ON u.id = p.user_id
            WHERE u.id = ?
        """, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        res = dict(row)
        if res.get("raw_attributes_json"):
            try:
                res["raw_attributes"] = json.loads(res["raw_attributes_json"])
            except Exception:
                res["raw_attributes"] = {}
        return res


def update_citizen_profile(user_id: int, profile_data: Dict[str, Any]) -> bool:
    """Updates or inserts a citizen profile for a given user, including personal user table fields."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Update users table if personal or geographical fields are provided
        user_field_map = {
            "full_name": profile_data.get("full_name"),
            "email": profile_data.get("email"),
            "phone": profile_data.get("phone"),
            "state": profile_data.get("state"),
            "district": profile_data.get("district")
        }
        user_updates = []
        user_params = []
        for field, val in user_field_map.items():
            if val is not None:
                user_updates.append(f"{field} = ?")
                user_params.append(val)
        if user_updates:
            user_params.append(user_id)
            cursor.execute(f"UPDATE users SET {', '.join(user_updates)} WHERE id = ?", user_params)

        raw_json = json.dumps(profile_data.get("raw_attributes", {}))
        cursor.execute("""
            INSERT INTO citizen_profiles (
                user_id, age, gender, occupation, annual_income, social_category,
                marital_status, is_differently_abled, land_ownership_hectares,
                residence_area, family_members_count, is_bpl, raw_attributes_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                age=excluded.age,
                gender=excluded.gender,
                occupation=excluded.occupation,
                annual_income=excluded.annual_income,
                social_category=excluded.social_category,
                marital_status=excluded.marital_status,
                is_differently_abled=excluded.is_differently_abled,
                land_ownership_hectares=excluded.land_ownership_hectares,
                residence_area=excluded.residence_area,
                family_members_count=excluded.family_members_count,
                is_bpl=excluded.is_bpl,
                raw_attributes_json=excluded.raw_attributes_json,
                updated_at=CURRENT_TIMESTAMP
        """, (
            user_id,
            profile_data.get("age", 35),
            profile_data.get("gender", "Male"),
            profile_data.get("occupation", "Worker"),
            profile_data.get("annual_income", 120000),
            profile_data.get("social_category", "OBC"),
            profile_data.get("marital_status", "Married"),
            1 if profile_data.get("is_differently_abled") else 0,
            profile_data.get("land_ownership_hectares", 0.0),
            profile_data.get("residence_area", "Urban"),
            profile_data.get("family_members_count", 4),
            1 if profile_data.get("is_bpl") else 0,
            raw_json
        ))
        conn.commit()
        return True


def update_user_language(user_id: int, language: str) -> bool:
    """Persists user's preferred language in profile raw_attributes."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT raw_attributes_json FROM citizen_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        raw = {}
        if row and row["raw_attributes_json"]:
            try:
                raw = json.loads(row["raw_attributes_json"])
            except Exception:
                raw = {}
        raw["preferred_language"] = language
        cursor.execute("""
            INSERT INTO citizen_profiles (user_id, raw_attributes_json, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                raw_attributes_json = excluded.raw_attributes_json,
                updated_at = CURRENT_TIMESTAMP
        """, (user_id, json.dumps(raw)))
        conn.commit()
        return True



# ==========================================
# Schemes CRUD
# ==========================================

def get_all_schemes(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetches all schemes from SQLite, optionally filtered by category."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if category and category.lower() != "all":
            cursor.execute("SELECT * FROM schemes WHERE category = ? ORDER BY id ASC", (category,))
        else:
            cursor.execute("SELECT * FROM schemes ORDER BY id ASC")
        rows = cursor.fetchall()
        schemes = []
        for r in rows:
            item = dict(r)
            try:
                item["eligibility_criteria"] = json.loads(item["eligibility_criteria_json"])
            except Exception:
                item["eligibility_criteria"] = {}
            try:
                item["required_documents"] = json.loads(item["required_documents_json"])
            except Exception:
                item["required_documents"] = []
            item["scheme_id"] = item.get("id")
            schemes.append(item)
        return schemes


def get_scheme_by_id(scheme_id: Any) -> Optional[Dict[str, Any]]:
    """Fetches single scheme by ID."""
    if scheme_id is None:
        return None
    try:
        scheme_id_int = int(scheme_id)
    except (ValueError, TypeError):
        return None

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schemes WHERE id = ?", (scheme_id_int,))
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        try:
            item["eligibility_criteria"] = json.loads(item["eligibility_criteria_json"])
        except Exception:
            item["eligibility_criteria"] = {}
        try:
            item["required_documents"] = json.loads(item["required_documents_json"])
        except Exception:
            item["required_documents"] = []
        item["scheme_id"] = item.get("id")
        return item


def get_scheme_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Fetches single scheme by unique code."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schemes WHERE code = ?", (code,))
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        try:
            item["eligibility_criteria"] = json.loads(item["eligibility_criteria_json"])
        except Exception:
            item["eligibility_criteria"] = {}
        try:
            item["required_documents"] = json.loads(item["required_documents_json"])
        except Exception:
            item["required_documents"] = []
        item["scheme_id"] = item.get("id")
        return item


# ==========================================
# User Demo Documents CRUD
# ==========================================

def get_user_documents(user_id: int) -> List[Dict[str, Any]]:
    """Lists all verified demo documents uploaded/generated for a user."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM user_documents WHERE user_id = ? ORDER BY created_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        docs = []
        for r in rows:
            d = dict(r)
            try:
                d["verified_ocr_data"] = json.loads(d.get("verified_ocr_data_json", "{}"))
            except Exception:
                d["verified_ocr_data"] = {}
            docs.append(d)
        return docs


def add_user_document(
    user_id: int,
    doc_type: str,
    doc_name: str,
    ocr_data: Dict[str, Any],
    file_path: str = "",
    status: str = "VERIFIED_DEMO"
) -> Dict[str, Any]:
    """Adds a new document record for a citizen with the given status."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_documents (user_id, doc_type, doc_name, file_path, status, verified_ocr_data_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, doc_type, doc_name, file_path, status, json.dumps(ocr_data)))
        doc_id = cursor.lastrowid
        conn.commit()
        return {
            "id": doc_id,
            "user_id": user_id,
            "doc_type": doc_type,
            "doc_name": doc_name,
            "status": status,
            "verified_ocr_data": ocr_data,
            "file_path": file_path,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def delete_user_document(doc_id: int, user_id: int) -> bool:
    """Deletes a specific document belonging to a user. Returns True if deleted."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM user_documents WHERE id = ? AND user_id = ?
        """, (doc_id, user_id))
        conn.commit()
        return cursor.rowcount > 0


# ==========================================
# Applications & Tracking Timeline CRUD
# ==========================================

def create_application(
    user_id: int,
    scheme_id: int,
    reference_no: str,
    applicant_data: Dict[str, Any],
    eligibility_answers: List[Any],
    draft_summary: str,
    notes: str = ""
) -> Dict[str, Any]:
    """Creates a simulated application submission with initial tracking timeline."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timeline = [
        {
            "step": 1,
            "title": "Application Submitted (Demo Mode)",
            "timestamp": now_str,
            "status": "COMPLETED",
            "remarks": "Draft verified and explicitly confirmed by citizen via JanSetu Agentic Workforce."
        },
        {
            "step": 2,
            "title": "Automated Document Pre-Screening",
            "timestamp": now_str,
            "status": "COMPLETED",
            "remarks": "Simulated OCR verification passed for identity & residency proof."
        },
        {
            "step": 3,
            "title": "Nodal Officer Desk Scrutiny",
            "timestamp": "Simulated in progress (Est. 2-3 days)",
            "status": "IN_PROGRESS",
            "remarks": "Assigned to District Welfare Officer for sanction appraisal."
        },
        {
            "step": 4,
            "title": "Field Verification / Benefit Disbursement",
            "timestamp": "Upcoming",
            "status": "PENDING",
            "remarks": "Direct Benefit Transfer (DBT) credit to Aadhaar-linked account."
        }
    ]

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications (
                reference_no, user_id, scheme_id, status, applicant_data_json,
                eligibility_answers_json, draft_summary, tracking_history_json, notes
            ) VALUES (?, ?, ?, 'SUBMITTED', ?, ?, ?, ?, ?)
        """, (
            reference_no,
            user_id,
            scheme_id,
            json.dumps(applicant_data),
            json.dumps(eligibility_answers),
            draft_summary,
            json.dumps(timeline),
            notes
        ))
        app_id = cursor.lastrowid

        # Also create a success notification
        cursor.execute("""
            INSERT INTO notifications (user_id, application_id, title, message, type)
            VALUES (?, ?, ?, ?, 'SUCCESS')
        """, (
            user_id,
            app_id,
            f"Application Submitted: {reference_no}",
            f"Your application for scheme #{scheme_id} was submitted in demo mode. Track progress using Ref #{reference_no}."
        ))

        conn.commit()

        return {
            "id": app_id,
            "reference_no": reference_no,
            "user_id": user_id,
            "scheme_id": scheme_id,
            "status": "SUBMITTED",
            "tracking_history": timeline,
            "draft_summary": draft_summary
        }


def get_user_applications(user_id: int) -> List[Dict[str, Any]]:
    """Returns all applications filed by a user."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as scheme_name, s.code as scheme_code, s.category as scheme_category,
                   s.benefits as scheme_benefits
            FROM applications a
            JOIN schemes s ON a.scheme_id = s.id
            WHERE a.user_id = ?
            ORDER BY a.submitted_at DESC
        """, (user_id,))
        rows = cursor.fetchall()
        apps = []
        for r in rows:
            item = dict(r)
            try:
                item["applicant_data"] = json.loads(item.get("applicant_data_json", "{}"))
            except Exception:
                item["applicant_data"] = {}
            try:
                item["tracking_history"] = json.loads(item.get("tracking_history_json", "[]"))
            except Exception:
                item["tracking_history"] = []
            try:
                item["eligibility_answers"] = json.loads(item.get("eligibility_answers_json", "[]"))
            except Exception:
                item["eligibility_answers"] = []
            item["application_ref"] = item.get("reference_no")
            item["created_at"] = item.get("submitted_at")
            apps.append(item)
        return apps


def get_application_by_ref(reference_no: str) -> Optional[Dict[str, Any]]:
    """Retrieves single application with scheme details by reference number."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, s.name as scheme_name, s.code as scheme_code, s.ministry as scheme_ministry,
                   s.category as scheme_category, s.benefits as scheme_benefits
            FROM applications a
            JOIN schemes s ON a.scheme_id = s.id
            WHERE a.reference_no = ?
        """, (reference_no,))
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        try:
            item["applicant_data"] = json.loads(item.get("applicant_data_json", "{}"))
        except Exception:
            item["applicant_data"] = {}
        try:
            item["tracking_history"] = json.loads(item.get("tracking_history_json", "[]"))
        except Exception:
            item["tracking_history"] = []
        item["application_ref"] = item.get("reference_no")
        item["created_at"] = item.get("submitted_at")
        return item


# ==========================================
# Notifications CRUD
# ==========================================

def get_user_notifications(user_id: int) -> List[Dict[str, Any]]:
    """Fetches user notifications."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC
        """, (user_id,))
        return [dict(r) for r in cursor.fetchall()]


# ==========================================
# Chat History CRUD
# ==========================================

def save_chat_message(session_id: str, sender: str, message: str, user_id: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
    """Saves a message to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (session_id, user_id, sender, message, metadata_json)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, user_id, sender, message, json.dumps(metadata or {})))
        conn.commit()


def get_chat_history(session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Fetches conversation history for a given session."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender, message, created_at, metadata_json
            FROM chat_history
            WHERE session_id = ?
            ORDER BY id ASC
            LIMIT ?
        """, (session_id, limit))
        rows = cursor.fetchall()
        msgs = []
        for r in rows:
            m = dict(r)
            try:
                m["metadata"] = json.loads(m.get("metadata_json", "{}"))
            except Exception:
                m["metadata"] = {}
            msgs.append(m)
        return msgs


def get_user_by_username_or_email(identifier: str) -> Optional[Dict[str, Any]]:
    """Retrieves a user by username or email."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM users
            WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)
            LIMIT 1
        """, (identifier.strip(), identifier.strip()))
        row = cursor.fetchone()
        if not row:
            return None
        return get_user_by_id(row["id"])


def create_citizen_user(
    username: str,
    full_name: str,
    email: str,
    phone: str = "",
    state: str = "Rajasthan",
    district: str = "Jaipur",
    profile_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Creates a new citizen user with linked demographic profile."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, full_name, email, phone, state, district)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, full_name, email, phone, state, district))
        user_id = cursor.lastrowid
        conn.commit()

    p_data = profile_data or {}
    update_citizen_profile(user_id, {
        "age": p_data.get("age") if p_data.get("age") is not None else 30,
        "gender": p_data.get("gender") or "Other",
        "occupation": p_data.get("occupation") or "Citizen",
        "annual_income": p_data.get("annual_income") if p_data.get("annual_income") is not None else 0.0,
        "social_category": p_data.get("social_category") or "General",
        "marital_status": p_data.get("marital_status") or "Single",
        "is_differently_abled": bool(p_data.get("is_differently_abled")),
        "land_ownership_hectares": p_data.get("land_ownership_hectares") if p_data.get("land_ownership_hectares") is not None else 0.0,
        "residence_area": p_data.get("residence_area") or "Urban",
        "family_members_count": p_data.get("family_members_count") if p_data.get("family_members_count") is not None else 1,
        "is_bpl": bool(p_data.get("is_bpl")),
        "raw_attributes": p_data.get("raw_attributes", {})
    })
    return get_user_by_id(user_id)


