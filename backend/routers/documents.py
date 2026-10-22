"""
JanSetu Documents Routes
Handles document uploads (real file storage), demo auto-generation, viewing, and deletion.
"""

import os
import uuid
import mimetypes
import random
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from backend.db import (
    get_user_documents,
    add_user_document,
    get_user_by_id,
    get_document_by_id,
    delete_user_document
)
from backend.config import UPLOADS_DIR, PROJECT_ROOT

router = APIRouter(prefix="/api/documents", tags=["Documents"])

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB


class GenerateDemoDocRequest(BaseModel):
    user_id: int
    doc_type: str  # e.g., 'aadhaar', 'vending_certificate', 'income_certificate', 'land_record', 'bank_passbook'
    doc_name: Optional[str] = None


@router.get("/user/{user_id}")
def list_documents(user_id: int):
    """Returns all demo and uploaded documents for a citizen."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    docs = get_user_documents(user_id)
    return {"user_id": user_id, "count": len(docs), "documents": docs}


@router.get("/{doc_id}")
def get_single_document(doc_id: int):
    """Retrieves document record metadata by ID."""
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document": doc}


@router.get("/{doc_id}/file")
def view_document_file(doc_id: int, download: bool = Query(False)):
    """
    Safely opens or previews an uploaded document, or downloads it.
    If it's a demo generated document without a stored physical file, returns document metadata JSON.
    """
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = doc.get("file_path") or ""
    if not file_path:
        # Demo document without disk file
        return JSONResponse(
            status_code=200,
            content={
                "is_demo_generated": True,
                "message": "Demo document with simulated OCR metadata. No binary file stored.",
                "document": doc
            }
        )

    # Resolve actual filesystem path
    candidate_paths = [
        UPLOADS_DIR / os.path.basename(file_path),
        PROJECT_ROOT / file_path,
        PROJECT_ROOT / "backend" / file_path,
        PROJECT_ROOT / "database" / file_path
    ]
    resolved_path = None
    for p in candidate_paths:
        if p.exists() and p.is_file():
            resolved_path = p
            break

    if not resolved_path:
        # File path in DB but file missing from disk
        return JSONResponse(
            status_code=200,
            content={
                "is_demo_generated": True,
                "message": "Physical file record not found on disk; rendering simulated proof.",
                "document": doc
            }
        )

    mime_type, _ = mimetypes.guess_type(str(resolved_path))
    if not mime_type:
        mime_type = "application/octet-stream"

    filename = os.path.basename(file_path)
    disposition = "attachment" if download else "inline"

    return FileResponse(
        path=str(resolved_path),
        media_type=mime_type,
        headers={
            "Content-Disposition": f'{disposition}; filename="{filename}"'
        }
    )


@router.get("/{doc_id}/download")
def download_document_file(doc_id: int):
    """Downloads the document file."""
    return view_document_file(doc_id, download=True)


@router.delete("/{doc_id}")
def delete_document(doc_id: int, user_id: Optional[int] = Query(None)):
    """
    Deletes an uploaded or demo document by ID.
    Unlinks associated physical file from storage if present.
    """
    doc = get_document_by_id(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if user_id is not None and doc.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this document")

    file_path = delete_user_document(doc_id, user_id=user_id)

    # Safely remove physical file if stored
    if file_path:
        for candidate in [
            UPLOADS_DIR / os.path.basename(file_path),
            PROJECT_ROOT / file_path
        ]:
            try:
                if candidate.exists() and candidate.is_file():
                    os.remove(candidate)
                    break
            except Exception:
                pass

    return {
        "success": True,
        "message": f"Document '{doc.get('doc_name', 'Document')}' deleted successfully.",
        "deleted_id": doc_id
    }


@router.post("/upload")
async def upload_document(
    user_id: int = Form(...),
    doc_type: str = Form(...),
    doc_name: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    Accepts document file upload (PDF, JPG, JPEG, PNG), persists file to disk,
    records status as UPLOADED (Pending Verification), and returns the saved document record.
    """
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    original_filename = file.filename or "uploaded_document"
    ext = os.path.splitext(original_filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format '{ext}'. Only PDF, JPG, JPEG, and PNG files are supported."
        )

    # Read content and validate size
    try:
        content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {str(e)}")

    file_size = len(content)
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds maximum limit of 15MB. Please upload a smaller file."
        )

    # Ensure uploads directory exists
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate unique safe filename
    safe_basename = "".join(c for c in os.path.basename(original_filename) if c.isalnum() or c in "._- ")
    unique_filename = f"doc_{uuid.uuid4().hex[:8]}_{safe_basename}"
    save_path = UPLOADS_DIR / unique_filename

    try:
        with open(save_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save document to storage: {str(e)}")

    # Display name determination
    clean_name = (doc_name or "").strip()
    if not clean_name:
        category_label = doc_type.replace('_', ' ').title()
        clean_name = f"{category_label} ({original_filename})"

    # Prepare OCR / verification metadata
    # NOTE: Uploading a file does NOT mark it as verified automatically.
    # Verification status reflects the actual status (Pending Verification).
    ocr_metadata = {
        "file_name": original_filename,
        "saved_filename": unique_filename,
        "content_type": file.content_type or mimetypes.guess_type(original_filename)[0] or "application/octet-stream",
        "file_size_bytes": file_size,
        "file_size_formatted": f"{round(file_size / 1024, 1)} KB" if file_size < 1024 * 1024 else f"{round(file_size / (1024 * 1024), 2)} MB",
        "verification_status": "PENDING_VERIFICATION",
        "status_description": "Document uploaded successfully. Queued for statutory desk verification.",
        "extracted_name": user.get("full_name"),
        "doc_type_detected": doc_type,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    doc_record = add_user_document(
        user_id=user_id,
        doc_type=doc_type,
        doc_name=clean_name,
        ocr_data=ocr_metadata,
        file_path=f"uploads/{unique_filename}",
        status="UPLOADED",
        file_size=file_size
    )

    return {
        "success": True,
        "message": f"Document '{clean_name}' uploaded successfully. Status: Uploaded (Pending Verification).",
        "document": doc_record
    }


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


