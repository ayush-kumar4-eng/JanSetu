"""
JanSetu Demo Documents Routes
Handles mock document uploads and automatic sample document generation.
"""

import random
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from backend.db import get_user_documents, add_user_document, get_user_by_id

router = APIRouter(prefix="/api/documents", tags=["Demo Documents"])


class GenerateDemoDocRequest(BaseModel):
    user_id: int
    doc_type: str  # e.g., 'aadhaar', 'vending_certificate', 'income_certificate', 'land_record', 'bank_passbook'
    doc_name: Optional[str] = None


@router.get("/user/{user_id}")
def list_documents(user_id: int):
    """Returns all demo documents for a citizen."""
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
        ocr_data=template["ocr"]
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
    file: UploadFile = File(...)
):
    """
    Accepts dummy document file upload, simulates OCR verification, and saves demo record.
    """
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_name = file.filename or "demo_document.pdf"

    # Simulated OCR extraction
    simulated_ocr = {
        "file_name": file_name,
        "content_type": file.content_type,
        "extracted_name": user.get("full_name"),
        "ocr_confidence": 98.4,
        "verification_status": "VERIFIED_DEMO",
        "doc_type_detected": doc_type
    }

    doc_record = add_user_document(
        user_id=user_id,
        doc_type=doc_type,
        doc_name=f"{doc_type.replace('_', ' ').title()} - {file_name}",
        ocr_data=simulated_ocr,
        file_path=f"uploads/{file_name}"
    )

    return {
        "success": True,
        "message": f"File '{file_name}' received and verified with simulated OCR.",
        "document": doc_record
    }
