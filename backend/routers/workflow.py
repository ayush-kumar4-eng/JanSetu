"""
JanSetu 5-Agent Workflow Endpoints
Coordinates multi-stage agentic welfare navigation journey.
"""

import random
import time
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.db import (
    get_user_by_id,
    get_scheme_by_id,
    create_application
)
from backend.agents.workflow import (
    need_intake_agent,
    scheme_matcher_agent,
    eligibility_assessor_agent,
    document_readiness_agent,
    application_drafter_agent,
    run_full_workflow,
    WorkflowState
)

router = APIRouter(prefix="/api/workflow", tags=["Agentic Workflow"])


# ==========================================
# Request Models
# ==========================================

class IntakeMatchRequest(BaseModel):
    user_id: int
    user_query: str = Field(..., min_length=3, description="Citizen's stated need in plain language")


class AuditEligibilityRequest(BaseModel):
    user_id: int
    scheme_id: int


class AuditDocumentsRequest(BaseModel):
    user_id: int
    scheme_id: int


class GenerateDraftRequest(BaseModel):
    user_id: int
    scheme_id: int
    user_query: Optional[str] = "Welfare assistance"
    confirmed_criteria: Optional[List[str]] = []


class SubmitSimulatedRequest(BaseModel):
    user_id: int
    scheme_id: int
    explicit_approval: bool = Field(..., description="User explicit consent is mandatory")
    applicant_data: Dict[str, Any]
    eligibility_answers: Optional[List[Any]] = []
    draft_summary: str
    notes: Optional[str] = ""


class RunFullWorkflowRequest(BaseModel):
    user_id: int
    user_query: str
    selected_scheme_id: Optional[int] = None
    confirmed_criteria: Optional[List[str]] = []


# ==========================================
# Workflow Endpoints
# ==========================================

@router.post("/intake-and-match")
def intake_and_match(req: IntakeMatchRequest):
    """
    Stage 1 & 2: Need Intake Agent & Scheme Matcher Agent
    Parses conversational need and returns top 2-3 matched welfare schemes with match scores and rationales.
    """
    user = get_user_by_id(req.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Citizen profile not found")

    state: WorkflowState = {
        "user_id": req.user_id,
        "user_profile": user,
        "user_query": req.user_query,
        "selected_scheme_id": None,
        "selected_scheme": None,
        "intake_result": None,
        "recommendations": None,
        "eligibility_assessment": None,
        "document_readiness": None,
        "application_draft": None,
        "user_confirmed_criteria": [],
        "error": None
    }

    # 1. Run Need Intake Agent
    intake_out = need_intake_agent(state)
    state.update(intake_out)

    # 2. Run Scheme Matcher Agent
    matcher_out = scheme_matcher_agent(state)
    state.update(matcher_out)

    return {
        "user_id": req.user_id,
        "query": req.user_query,
        "intake_analysis": state.get("intake_result"),
        "recommendations": state.get("recommendations", []),
        "results": state.get("all_matches", state.get("recommendations", []))
    }


@router.post("/audit-eligibility")
def audit_eligibility(req: AuditEligibilityRequest):
    """
    Stage 3: Eligibility Assessor Agent
    Deeply compares citizen profile against selected scheme statutory criteria.
    """
    user = get_user_by_id(req.user_id)
    scheme = get_scheme_by_id(req.scheme_id)

    if not user:
        raise HTTPException(status_code=404, detail="Citizen profile not found")
    if not scheme:
        raise HTTPException(status_code=404, detail="Selected scheme not found")

    state: WorkflowState = {
        "user_id": req.user_id,
        "user_profile": user,
        "user_query": "",
        "selected_scheme_id": req.scheme_id,
        "selected_scheme": scheme,
        "intake_result": None,
        "recommendations": None,
        "eligibility_assessment": None,
        "document_readiness": None,
        "application_draft": None,
        "user_confirmed_criteria": [],
        "error": None
    }

    result = eligibility_assessor_agent(state)
    return {
        "scheme_id": req.scheme_id,
        "scheme_name": scheme["name"],
        "eligibility": result.get("eligibility_assessment")
    }


@router.post("/audit-documents")
def audit_documents(req: AuditDocumentsRequest):
    """
    Stage 4: Document Readiness Agent
    Audits user demo documents against scheme requirements, flagging Ready vs Missing.
    """
    user = get_user_by_id(req.user_id)
    scheme = get_scheme_by_id(req.scheme_id)

    if not user:
        raise HTTPException(status_code=404, detail="Citizen profile not found")
    if not scheme:
        raise HTTPException(status_code=404, detail="Selected scheme not found")

    state: WorkflowState = {
        "user_id": req.user_id,
        "user_profile": user,
        "user_query": "",
        "selected_scheme_id": req.scheme_id,
        "selected_scheme": scheme,
        "intake_result": None,
        "recommendations": None,
        "eligibility_assessment": None,
        "document_readiness": None,
        "application_draft": None,
        "user_confirmed_criteria": [],
        "error": None
    }

    result = document_readiness_agent(state)
    return {
        "scheme_id": req.scheme_id,
        "scheme_name": scheme["name"],
        "document_readiness": result.get("document_readiness")
    }


@router.post("/generate-draft")
def generate_draft(req: GenerateDraftRequest):
    """
    Stage 5: Application Drafter Agent
    Synthesizes citizen profile, verified documents, and confirmed rules into an official application draft.
    """
    user = get_user_by_id(req.user_id)
    scheme = get_scheme_by_id(req.scheme_id)

    if not user:
        raise HTTPException(status_code=404, detail="Citizen profile not found")
    if not scheme:
        raise HTTPException(status_code=404, detail="Selected scheme not found")

    # First check document readiness
    doc_state: WorkflowState = {
        "user_id": req.user_id,
        "user_profile": user,
        "user_query": req.user_query or "",
        "selected_scheme_id": req.scheme_id,
        "selected_scheme": scheme,
        "intake_result": None,
        "recommendations": None,
        "eligibility_assessment": None,
        "document_readiness": None,
        "application_draft": None,
        "user_confirmed_criteria": req.confirmed_criteria or [],
        "error": None
    }
    doc_res = document_readiness_agent(doc_state)
    doc_state.update(doc_res)

    draft_res = application_drafter_agent(doc_state)
    return {
        "scheme_id": req.scheme_id,
        "scheme_name": scheme["name"],
        "application_draft": draft_res.get("application_draft")
    }


@router.post("/submit-simulated")
def submit_simulated_application(req: SubmitSimulatedRequest):
    """
    Stage 6: Simulated Application Submission
    Requires explicit user approval. Issues reference number, sets up live tracking timeline and notification.
    """
    if not req.explicit_approval:
        raise HTTPException(
            status_code=400,
            detail="Safety Requirement: Explicit user confirmation and approval is required before submission."
        )

    user = get_user_by_id(req.user_id)
    scheme = get_scheme_by_id(req.scheme_id)

    if not user:
        raise HTTPException(status_code=404, detail="Citizen profile not found")
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")

    # Generate realistic simulated reference number: JS-2025-XXXXX
    rand_digits = random.randint(10000, 99999)
    reference_no = f"JS-2025-{rand_digits}"

    app_record = create_application(
        user_id=req.user_id,
        scheme_id=req.scheme_id,
        reference_no=reference_no,
        applicant_data=req.applicant_data,
        eligibility_answers=req.eligibility_answers or [],
        draft_summary=req.draft_summary,
        notes=req.notes or ""
    )

    return {
        "success": True,
        "message": "Application submitted in simulated demo mode.",
        "reference_no": reference_no,
        "application_ref": reference_no,
        "application": app_record,
        "disclaimer": "⚠️ JanSetu is a hackathon demonstration prototype. No actual government submission occurred."
    }


@router.post("/run-full")
def run_entire_workflow(req: RunFullWorkflowRequest):
    """Executes the complete compiled LangGraph 5-agent state graph pipeline."""
    try:
        final_state = run_full_workflow(
            user_id=req.user_id,
            user_query=req.user_query,
            selected_scheme_id=req.selected_scheme_id,
            user_confirmed_criteria=req.confirmed_criteria
        )
        return {
            "success": True,
            "user_id": req.user_id,
            "intake_result": final_state.get("intake_result"),
            "recommendations": final_state.get("recommendations", []),
            "eligibility": final_state.get("eligibility_assessment"),
            "document_readiness": final_state.get("document_readiness"),
            "application_draft": final_state.get("application_draft")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LangGraph execution error: {str(e)}")
