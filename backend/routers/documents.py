"""
JanSetu Documents Routes
Handles document uploads (real file storage), demo auto-generation, viewing, and deletion.
"""

import os
import random
import shutil
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.db import get_user_documents, add_user_document, get_user_by_id, delete_user_document
from backend.config import UPLOADS_DIR

router = APIRouter(prefix="/api/documents", tags=["Documents"])

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}


class GenerateDemoDocRequest(BaseModel):
    user_id: int
    doc_type: str  # e.g., 'aadhaar', 'vending_certificate', 'income_certificate', 'land_record', 'bank_passbook'
    doc_name: Optional[str] = None


@router.get("/user/{user_id}")
def list_documents(user_id: int):
    """Returns all documents for a citizen."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    docs = get_user_documents(user_id)
    return {"user_id": user_id, "count": len(docs), "documents": docs}


@router.post("/generate-demo")
def generate_sample_document(req: GenerateDemoDocRequest):
    """Generates an instant sample demo document with simulated OCR data."""
    user = get_user_by_id(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_name = user.get("full_name", "Citizen")
    doc_type = req.doc_type.lower()

    # Pre-configure realistic simulated OCR metadata
    ocr_templates = {
        "aadhaar": {
            "name": req.doc_name or "Aadhaar Card (Masked Demo)",
            "ocr": {
                "doc_type": "Aadhaar Card",
                "aadhaar_masked": f"XXXX-XXXX-{random.randint(1000, 9999)}",
                "holder_name": user_name,
                "dob": f"19{random.randint(70, 99)}-0{random.randint(1, 9)}-{random.randint(10, 28)}",
                "gender": user.get("gender", "Male"),
                "state": user.get("state", "Rajasthan"),
                "status": "VALID_VERIFIED_DEMO"
            }
        },
        "vending_certificate": {
            "name": req.doc_name or "Certificate of Vending / LoR (Demo)",
            "ocr": {
                "doc_type": "Certificate of Vending",
                "cov_number": f"ULB-COV-2024-{random.randint(1000, 9999)}",
                "vendor_name": user_name,
                "vending_zone": f"Ward {random.randint(10, 50)}, {user.get('district', 'Jaipur')}",
                "validity": "2028-12-31",
                "status": "ACTIVE_REGISTERED"
            }
        },
        "income_certificate": {
            "name": req.doc_name or "Tehsildar Income Certificate (Demo)",
            "ocr": {
                "doc_type": "Income Certificate",
                "cert_id": f"INC-REV-2025-{random.randint(10000, 99999)}",
                "applicant_name": user_name,
                "certified_annual_income": user.get("annual_income", 120000),
                "issuing_authority": f"Tehsildar Office, {user.get('district', 'Jaipur')}",
                "financial_year": "2024-2025"
            }
        },
        "land_record": {
            "name": req.doc_name or "Khasra / Jamabandi Land Record (Demo)",
            "ocr": {
                "doc_type": "RoR Land Record",
                "khasra_no": f"{random.randint(100, 450)}/{random.randint(1, 4)}",
                "owner_name": user_name,
                "land_area_hectares": user.get("land_ownership_hectares", 1.2),
                "classification": "Irrigated Agricultural",
                "district": user.get("district", "Dausa")
            }
        },
        "bank_passbook": {
            "name": req.doc_name or "Bank Account Passbook (Demo)",
            "ocr": {
                "doc_type": "Bank Passbook",
                "bank_name": "State Bank of India",
                "account_masked": f"XXXXXXXX{random.randint(1000, 9999)}",
                "account_holder": user_name,
                "ifsc": "SBIN0001420",
                "dbt_seeded": True
            }
        },
        "caste_certificate": {
            "name": req.doc_name or "Social Category / Caste Certificate (Demo)",
            "ocr": {
                "doc_type": "Caste Certificate",
                "certificate_no": f"CC-{random.randint(100000, 999999)}",
                "candidate_name": user_name,
                "category": user.get("social_category", "OBC"),
                "state": user.get("state", "Rajasthan")
            }
        }
    }

    template = ocr_templates.get(doc_type, {
        "name": req.doc_name or f"{req.doc_type.replace('_', ' ').title()} (Demo)",
        "ocr": {
            "doc_type": req.doc_type,
            "holder_name": user_name,
            "verification_status": "DEMO_VERIFIED"
        }
    })

    saved = add_user_document(
        user_id=req.user_id,
        doc_type=doc_type,
        doc_name=template["name"],
        ocr_data=template["ocr"],
        status="VERIFIED_DEMO"
    )

    return {
        "success": True,
        "message": f"Demo document '{template['name']}' generated and verified successfully.",
        "document": saved
    }


@router.post("/generate-demo/{user_id}")
def generate_sample_document_for_user(user_id: int, doc_type: str = "aadhaar", doc_name: Optional[str] = None):
    """Generates an instant sample demo document using path user_id and query params."""
    req = GenerateDemoDocRequest(user_id=user_id, doc_type=doc_type, doc_name=doc_name)
    return generate_sample_document(req)


@router.post("/upload")
async def upload_document(
    user_id: int = Form(...),
    doc_type: str = Form(...),
    doc_name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Accepts a real document file upload (PDF/JPG/PNG).
    Saves the file to disk, records it as PENDING_REVIEW so it does NOT auto-verify.
    The display name is chosen by the user.
    """
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not doc_name or not doc_name.strip():
        raise HTTPException(status_code=400, detail="Document display name is required.")

    original_filename = file.filename or "document"
    ext = Path(original_filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: PDF, JPG, JPEG, PNG."
        )

    # Build safe storage filename: user_<id>_<random>_<doctype><ext>
    safe_filename = f"user_{user_id}_{random.randint(10000, 99999)}_{doc_type}{ext}"
    user_upload_dir = UPLOADS_DIR / str(user_id)
    user_upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = user_upload_dir / safe_filename

    # Stream-save to disk
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File storage error: {str(e)}")

    relative_path = f"uploads/{user_id}/{safe_filename}"

    doc_record = add_user_document(
        user_id=user_id,
        doc_type=doc_type,
        doc_name=doc_name.strip(),
        ocr_data={
            "original_filename": original_filename,
            "content_type": file.content_type,
            "note": "Uploaded by citizen. Awaiting verification."
        },
        file_path=relative_path,
        status="PENDING_REVIEW"
    )

    return {
        "success": True,
        "message": f"Document '{doc_name.strip()}' uploaded successfully. It is pending review.",
        "document": doc_record
    }


@router.get("/view/{doc_id}")
def view_document(doc_id: int, user_id: int):
    """
    Serves the actual uploaded file for viewing/downloading.
    Only the document owner can access it.
    """
    from backend.db import get_db_connection
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_documents WHERE id = ? AND user_id = ?",
            (doc_id, user_id)
        )
        row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Document not found or access denied.")

    doc = dict(row)
    file_path_str = doc.get("file_path", "")
    if not file_path_str:
        raise HTTPException(status_code=404, detail="No physical file found for this document (demo-generated).")

    # Try absolute path first, then relative to project root
    abs_path = Path(file_path_str)
    if not abs_path.is_absolute():
        from backend.config import PROJECT_ROOT
        abs_path = PROJECT_ROOT / file_path_str

    if not abs_path.exists():
        raise HTTPException(status_code=404, detail="Physical file no longer exists on server.")

    return FileResponse(
        path=str(abs_path),
        filename=Path(file_path_str).name,
        media_type="application/octet-stream"
    )


@router.delete("/{doc_id}")
def delete_document(doc_id: int, user_id: int):
    """
    Deletes a document record (and its physical file if any) for the owning user.
    """
    # Fetch the document first to get the file path
    from backend.db import get_db_connection
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_documents WHERE id = ? AND user_id = ?",
            (doc_id, user_id)
        )
        row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Document not found or access denied.")

    doc = dict(row)
    file_path_str = doc.get("file_path", "")

    # Delete physical file if it exists
    if file_path_str:
        abs_path = Path(file_path_str)
        if not abs_path.is_absolute():
            from backend.config import PROJECT_ROOT
            abs_path = PROJECT_ROOT / file_path_str
        if abs_path.exists():
            try:
                abs_path.unlink()
            except Exception:
                pass  # Non-fatal: still delete the DB record

    # Delete from DB
    deleted = delete_user_document(doc_id, user_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete document record.")

    return {
        "success": True,
        "message": f"Document '{doc.get('doc_name', '')}' deleted successfully.",
        "deleted_id": doc_id
    }
