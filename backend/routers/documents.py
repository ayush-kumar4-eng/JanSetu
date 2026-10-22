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
    target_requirement: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    Accepts a real document file upload (PDF/JPG/PNG).
    Saves the file to disk and records it as VERIFIED in the citizen locker.
    Links target_requirement so workflow stages can immediately satisfy readiness.
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

    relative_path = f"backend/uploads/{user_id}/{safe_filename}"

    clean_target_req = (target_requirement or doc_name).strip()

    doc_record = add_user_document(
        user_id=user_id,
        doc_type=doc_type,
        doc_name=doc_name.strip(),
        ocr_data={
            "original_filename": original_filename,
            "content_type": file.content_type,
            "target_requirement": clean_target_req,
            "note": "Uploaded by citizen and verified."
        },
        file_path=relative_path,
        status="VERIFIED"
    )

    return {
        "success": True,
        "message": f"Document '{doc_name.strip()}' uploaded and verified successfully!",
        "document": doc_record
    }


@router.get("/view/{doc_id}")
def view_document(doc_id: int, user_id: int):
    """
    Serves the actual uploaded file for inline viewing/downloading.
    If the document is demo-generated, generates a verified digital e-Document view.
    """
    import json
    from fastapi.responses import HTMLResponse
    from backend.db import get_db_connection
    from backend.config import PROJECT_ROOT, BACKEND_DIR, UPLOADS_DIR

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
    file_path_str = (doc.get("file_path") or "").strip()

    # 1. Check if a physical file exists in any candidate location
    abs_path = None
    if file_path_str:
        p = Path(file_path_str)
        if p.is_absolute() and p.exists():
            abs_path = p
        else:
            candidates = [
                PROJECT_ROOT / file_path_str,
                BACKEND_DIR / file_path_str,
                UPLOADS_DIR / str(user_id) / p.name,
                UPLOADS_DIR / p.name,
                PROJECT_ROOT / "backend" / file_path_str
            ]
            for c in candidates:
                if c.exists():
                    abs_path = c
                    break

    # If physical file found, stream with inline disposition
    if abs_path and abs_path.exists():
        ext = abs_path.suffix.lower()
        if ext == ".pdf":
            media_type = "application/pdf"
        elif ext == ".png":
            media_type = "image/png"
        elif ext in [".jpg", ".jpeg"]:
            media_type = "image/jpeg"
        else:
            media_type = "application/octet-stream"

        return FileResponse(
            path=str(abs_path),
            media_type=media_type,
            headers={
                "Content-Disposition": f'inline; filename="{abs_path.name}"'
            }
        )

    # 2. If no physical file (Demo Generated Document), render verified Digital Credential
    ocr_raw = doc.get("verified_ocr_data_json") or "{}"
    try:
        ocr_data = json.loads(ocr_raw) if isinstance(ocr_raw, str) else ocr_raw
    except Exception:
        ocr_data = {}

    user = get_user_by_id(user_id) or {}
    user_name = user.get("full_name") or user.get("username") or "Verified Citizen"
    doc_title = doc.get("doc_name") or "Government Welfare Document"
    doc_type = (doc.get("doc_type") or "Document").replace("_", " ").title()
    created_at = doc.get("created_at") or "2026-10-22"

    rows_html = ""
    for k, v in ocr_data.items():
        if k in ["original_filename", "content_type", "note"]:
            continue
        key_label = k.replace("_", " ").title()
        rows_html += f"""
        <tr>
            <td style="padding: 10px 14px; font-weight: 600; color: #1e3a8a; border-bottom: 1px solid #e2e8f0; width: 40%;">{key_label}</td>
            <td style="padding: 10px 14px; color: #1e293b; border-bottom: 1px solid #e2e8f0;">{v}</td>
        </tr>
        """

    if not rows_html:
        rows_html = f"""
        <tr>
            <td style="padding: 10px 14px; font-weight: 600; color: #1e3a8a; border-bottom: 1px solid #e2e8f0;">Citizen Name</td>
            <td style="padding: 10px 14px; color: #1e293b; border-bottom: 1px solid #e2e8f0;">{user_name}</td>
        </tr>
        <tr>
            <td style="padding: 10px 14px; font-weight: 600; color: #1e3a8a; border-bottom: 1px solid #e2e8f0;">Occupation</td>
            <td style="padding: 10px 14px; color: #1e293b; border-bottom: 1px solid #e2e8f0;">{user.get('occupation', 'Citizen')}</td>
        </tr>
        <tr>
            <td style="padding: 10px 14px; font-weight: 600; color: #1e3a8a; border-bottom: 1px solid #e2e8f0;">District & State</td>
            <td style="padding: 10px 14px; color: #1e293b; border-bottom: 1px solid #e2e8f0;">{user.get('district', 'Jaipur')}, {user.get('state', 'Rajasthan')}</td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JanSetu e-Locker — {doc_title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 30px 20px;
            display: flex;
            justify-content: center;
        }}
        .cert-card {{
            background: #ffffff;
            border-radius: 12px;
            max-width: 680px;
            width: 100%;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);
            overflow: hidden;
            border: 1px solid #cbd5e1;
            position: relative;
        }}
        .cert-header {{
            background: linear-gradient(135deg, #0f2c59 0%, #1e3a8a 100%);
            color: #ffffff;
            padding: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .cert-header-left {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}
        .cert-header-left i {{
            font-size: 32px;
            color: #f59e0b;
        }}
        .cert-header-title {{
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        .cert-header-sub {{
            font-size: 12px;
            color: #cbd5e1;
        }}
        .cert-badge {{
            background: #065f46;
            color: #d1fae5;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}
        .cert-body {{
            padding: 28px;
        }}
        .doc-title-row {{
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 14px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .doc-title-row h2 {{
            margin: 0;
            font-size: 22px;
            color: #0f2c59;
        }}
        .doc-meta {{
            font-size: 12px;
            color: #64748b;
        }}
        .details-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
            font-size: 13.5px;
        }}
        .cert-seal-box {{
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 8px;
            padding: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .seal-info {{
            font-size: 12px;
            color: #475569;
            line-height: 1.5;
        }}
        .seal-qr {{
            width: 60px;
            height: 60px;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: #0f2c59;
        }}
        .cert-footer {{
            background: #f8fafc;
            padding: 16px 24px;
            border-top: 1px solid #e2e8f0;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }}
        .btn {{
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
        }}
        .btn-print {{
            background: #0f2c59;
            color: #ffffff;
        }}
        .btn-close {{
            background: #e2e8f0;
            color: #334155;
        }}
    </style>
</head>
<body>
    <div class="cert-card">
        <div class="cert-header">
            <div class="cert-header-left">
                <i class="fa-solid fa-landmark-flag"></i>
                <div>
                    <div class="cert-header-title">जनसेतु — JanSetu National Welfare Portal</div>
                    <div class="cert-header-sub">Government of India Digital Locker Verified Credential</div>
                </div>
            </div>
            <div class="cert-badge">
                <i class="fa-solid fa-circle-check"></i> Digitally Verified
            </div>
        </div>

        <div class="cert-body">
            <div class="doc-title-row">
                <div>
                    <h2>{doc_title}</h2>
                    <div class="doc-meta">Category: {doc_type} • Issued To: <strong>{user_name}</strong></div>
                </div>
                <div class="doc-meta">Record ID: #{doc.get('id', 1)}</div>
            </div>

            <table class="details-table">
                {rows_html}
            </table>

            <div class="cert-seal-box">
                <div class="seal-info">
                    <strong><i class="fa-solid fa-fingerprint"></i> JanSetu Cryptographic Verification Token:</strong><br>
                    UID-JS-{doc.get('id', 1)}-{random.randint(100000, 999999)}<br>
                    Issued on: {created_at} • Status: Active & Authentic
                </div>
                <div class="seal-qr">
                    <i class="fa-solid fa-qrcode"></i>
                </div>
            </div>
        </div>

        <div class="cert-footer">
            <button class="btn btn-print" onclick="window.print()">
                <i class="fa-solid fa-print"></i> Print / Save as PDF
            </button>
            <button class="btn btn-close" onclick="window.close()">
                <i class="fa-solid fa-xmark"></i> Close
            </button>
        </div>
    </div>
</body>
</html>"""
    return HTMLResponse(content=html_content)


@router.delete("/{doc_id}")
def delete_document(doc_id: int, user_id: int):
    """
    Deletes a document record (and its physical file if any) for the owning user.
    """
    from backend.db import get_db_connection
    from backend.config import PROJECT_ROOT, BACKEND_DIR, UPLOADS_DIR

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
    file_path_str = (doc.get("file_path") or "").strip()

    # Delete physical file if it exists in any location
    if file_path_str:
        p = Path(file_path_str)
        candidates = [
            p if p.is_absolute() else None,
            PROJECT_ROOT / file_path_str,
            BACKEND_DIR / file_path_str,
            UPLOADS_DIR / str(user_id) / p.name,
            UPLOADS_DIR / p.name,
            PROJECT_ROOT / "backend" / file_path_str
        ]
        for c in candidates:
            if c and c.exists():
                try:
                    c.unlink()
                except Exception:
                    pass
                break

    # Delete from DB
    deleted = delete_user_document(doc_id, user_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete document record.")

    return {
        "success": True,
        "message": f"Document '{doc.get('doc_name', '')}' deleted successfully.",
        "deleted_id": doc_id
    }
