"""
JanSetu LangGraph Multi-Agent Workflow
Coordinates 5 Specialized Agents:
1. Need Intake Agent
2. Scheme Matcher Agent
3. Eligibility Assessor Agent
4. Document Readiness Agent
5. Application Drafter Agent
"""

import json
import logging
from typing import Any, Dict, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from backend.llm_client import invoke_llm_json, invoke_llm
from backend.vector_search import search_schemes
from backend.db import get_scheme_by_id, get_user_documents, get_user_by_id

logger = logging.getLogger("JanSetu.WorkflowAgents")


# ==========================================
# Agent Workflow State Definition
# ==========================================

class WorkflowState(TypedDict):
    user_id: int
    user_profile: Dict[str, Any]
    user_query: str
    selected_scheme_id: Optional[int]
    selected_scheme: Optional[Dict[str, Any]]
    intake_result: Optional[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, Any]]]
    eligibility_assessment: Optional[Dict[str, Any]]
    document_readiness: Optional[Dict[str, Any]]
    application_draft: Optional[Dict[str, Any]]
    user_confirmed_criteria: Optional[List[str]]
    error: Optional[str]


# ==========================================
# Agent 1: Need Intake Agent
# ==========================================

def need_intake_agent(state: WorkflowState) -> Dict[str, Any]:
    """Analyzes citizen freeform natural language query and profile."""
    logger.info("Executing Agent 1: Need Intake Agent")
    query = state.get("user_query", "").strip()
    profile = state.get("user_profile", {})

    system_prompt = """
You are the Need Intake Agent of JanSetu, India's AI workforce for government welfare navigation.
Your job is to analyze the citizen's self-described need in plain conversational language,
combine it with their citizen profile, and extract structured welfare search parameters.
Respond in valid JSON format:
{
  "need_summary": "1-2 sentence concise summary of citizen situation and need",
  "identified_categories": ["Micro-Enterprise", "Agriculture", etc.],
  "key_intents": ["working capital loan", "crop loss compensation", etc.],
  "semantic_search_query": "Optimized dense search query capturing citizen intent, occupation, and financial need"
}
"""

    user_prompt = f"""
Citizen Profile:
- Name: {profile.get('full_name')}
- Age: {profile.get('age')}, Gender: {profile.get('gender')}
- Occupation: {profile.get('occupation')}
- Annual Income: Rs {profile.get('annual_income')}
- Social Category: {profile.get('social_category')}
- Location: {profile.get('residence_area')}, {profile.get('district')}, {profile.get('state')}
- Land Ownership: {profile.get('land_ownership_hectares')} hectares
- BPL Status: {'Yes' if profile.get('is_bpl') else 'No'}

Citizen's Plain Language Query:
"{query}"
"""

    intake_data = invoke_llm_json(user_prompt, system_prompt)

    # Fallback search query if LLM did not return one
    semantic_query = intake_data.get("semantic_search_query")
    if not semantic_query or len(semantic_query) < 5:
        semantic_query = f"{query} financial assistance subsidy grant".strip()
        intake_data["semantic_search_query"] = semantic_query

    return {"intake_result": intake_data}


# ==========================================
# Agent 2: Scheme Matcher Agent
# ==========================================

def scheme_matcher_agent(state: WorkflowState) -> Dict[str, Any]:
    """Retrieves candidates via Qdrant semantic search and highlights top 2-3 recommendations."""
    logger.info("Executing Agent 2: Scheme Matcher Agent")
    intake = state.get("intake_result", {})
    query = intake.get("semantic_search_query") or state.get("user_query", "")
    profile = state.get("user_profile", {})

    # Semantic search with Qdrant - retrieve up to 7 candidates
    candidates = search_schemes(query, limit=7)

    # If fewer than 6 candidates found, supplement with user query / identified category
    if len(candidates) < 6:
        category_hint = intake.get("identified_category") or ""
        supp_query = f"{state.get('user_query', '')} {category_hint} welfare scheme financial assistance".strip()
        supp = search_schemes(supp_query, limit=7)
        for s in supp:
            sid = s.get("id") or s.get("scheme_id")
            s["id"] = sid
            s["scheme_id"] = sid
            if not any((c.get("id") == sid or c.get("scheme_id") == sid) for c in candidates):
                candidates.append(s)
            if len(candidates) >= 7:
                break

    # Normalize id and scheme_id across all candidates
    for c in candidates:
        sid = c.get("id") or c.get("scheme_id")
        c["id"] = sid
        c["scheme_id"] = sid

    system_prompt = """
You are the Scheme Matcher Agent for JanSetu.
Given a citizen's profile and top candidate government schemes from semantic search,
evaluate each candidate and select the top 2-3 best matching schemes.
For each recommended scheme, generate:
1. match_score (percentage 75-98 based on relevance)
2. match_rationale (Why this scheme specifically fits their occupation, income, and need)
3. key_highlight (The most attractive benefit for them)

Respond in JSON format:
{
  "recommendations": [
    {
      "scheme_id": <int>,
      "code": "<string>",
      "name": "<string>",
      "match_score": <number>,
      "match_rationale": "<string>",
      "key_highlight": "<string>"
    }
  ]
}
"""

    candidate_summaries = []
    for c in candidates[:6]:
        candidate_summaries.append({
            "scheme_id": c["scheme_id"],
            "code": c["code"],
            "name": c["name"],
            "category": c["category"],
            "benefits": c["benefits"],
            "target_audience": c.get("target_audience")
        })

    user_prompt = f"""
Citizen Profile:
- Occupation: {profile.get('occupation')}
- Income: Rs {profile.get('annual_income')}
- Area: {profile.get('residence_area')}, Category: {profile.get('social_category')}
- Need: {state.get('user_query')}

Candidate Schemes:
{json.dumps(candidate_summaries, indent=2)}
"""

    llm_recommendations = invoke_llm_json(user_prompt, system_prompt)
    recs_list = llm_recommendations.get("recommendations", [])
    rec_ids = {r.get("scheme_id") for r in recs_list if r.get("scheme_id")}

    # Build top recommendations
    final_recs = []
    seen_ids = set()

    for r in recs_list:
        scheme_id = r.get("scheme_id")
        if scheme_id and scheme_id not in seen_ids:
            full_scheme = get_scheme_by_id(scheme_id)
            if full_scheme:
                sid = full_scheme.get("id") or full_scheme.get("scheme_id")
                full_scheme["id"] = sid
                full_scheme["scheme_id"] = sid
                full_scheme["is_recommended"] = True
                full_scheme["match_score"] = r.get("match_score", 92)
                full_scheme["match_percentage"] = f"{int(r.get('match_score', 92))}%"
                full_scheme["match_rationale"] = r.get("match_rationale", "Strong match for your citizen profile and stated requirements.")
                full_scheme["key_highlight"] = r.get("key_highlight", full_scheme.get("benefits", "")[:90])
                final_recs.append(full_scheme)
                seen_ids.add(sid)

    # Ensure at least 2 recommended schemes from top candidates
    if len(final_recs) < 2 and candidates:
        for c in candidates:
            cid = c.get("id") or c.get("scheme_id")
            if cid not in seen_ids:
                c["id"] = cid
                c["scheme_id"] = cid
                c["is_recommended"] = True
                c["match_score"] = c.get("match_score", 85)
                c["match_percentage"] = f"{int(c.get('match_score', 85))}%"
                c["match_rationale"] = "Strong candidate identified from semantic alignment with your profile category."
                c["key_highlight"] = c.get("benefits", "")[:90]
                final_recs.append(c)
                seen_ids.add(cid)
                if len(final_recs) >= 3:
                    break

    # Build complete list of 6-7 results, tagging recommended vs other relevant matches
    all_results = []
    for r in final_recs[:3]:
        r["is_recommended"] = True
        all_results.append(r)

    for c in candidates:
        cid = c.get("id") or c.get("scheme_id")
        if cid not in seen_ids:
            full = get_scheme_by_id(cid) or c
            full["id"] = cid
            full["scheme_id"] = cid
            full["is_recommended"] = False
            full["match_score"] = c.get("match_score", 72)
            full["match_percentage"] = f"{int(c.get('match_score', 72))}%"
            full["match_rationale"] = "Relevant welfare scheme matching your sector and geographic applicability."
            full["key_highlight"] = full.get("benefits", "")[:90]
            all_results.append(full)
            seen_ids.add(cid)
            if len(all_results) >= 7:
                break

    return {
        "recommendations": final_recs[:3],
        "all_matches": all_results[:7]
    }


# ==========================================
# Agent 3: Eligibility Assessor Agent
# ==========================================

def eligibility_assessor_agent(state: WorkflowState) -> Dict[str, Any]:
    """Deeply audits citizen profile against chosen scheme rules."""
    logger.info("Executing Agent 3: Eligibility Assessor Agent")
    scheme = state.get("selected_scheme")
    if not scheme and state.get("selected_scheme_id"):
        scheme = get_scheme_by_id(state["selected_scheme_id"])

    profile = state.get("user_profile", {})
    if not scheme:
        return {"error": "No scheme selected for eligibility assessment."}

    user_id = state.get("user_id") or profile.get("id") or 1
    user_docs = get_user_documents(user_id)
    doc_summary = [f"{d.get('doc_name')} (Type: {d.get('doc_type')}, Status: {d.get('status')})" for d in user_docs]

    criteria = scheme.get("eligibility_criteria", {})
    key_rules = criteria.get("key_rules", [])

    system_prompt = """
You are the Eligibility Assessor Agent for JanSetu.
You must compare the citizen's profile and any uploaded supporting documents with the scheme's statutory eligibility criteria.
Evaluate each criterion and categorize as:
- 'PASSED': Profile meets criterion (e.g. age, income ceiling, occupation, location) or is substantiated by an uploaded supporting document.
- 'FAILED': Profile definitively violates rule without waiver.
- 'SELF_DECLARATION': Requires citizen's personal affirmation (e.g. 'I do not have a pucca house' or 'I have no active bank default').

Provide response in JSON:
{
  "verdict": "ELIGIBLE" or "CONDITIONALLY_ELIGIBLE" or "INELIGIBLE",
  "score": <0-100 percentage confidence>,
  "summary": "Clear, reassuring 1-2 sentence assessment for citizen",
  "rules_audit": [
    {
      "id": 1,
      "rule_text": "...",
      "status": "PASSED" | "FAILED" | "SELF_DECLARATION",
      "citizen_fact": "...",
      "explanation": "..."
    }
  ],
  "actionable_declarations": [
    "Checklist item 1 citizen needs to tick to confirm",
    "Checklist item 2"
  ]
}
"""

    user_prompt = f"""
Scheme Details:
- Name: {scheme.get('name')}
- Criteria Rules: {json.dumps(criteria, indent=2)}

Citizen Facts:
- Age: {profile.get('age')}
- Gender: {profile.get('gender')}
- Occupation: {profile.get('occupation')}
- Annual Income: Rs {profile.get('annual_income')}
- Land Ownership: {profile.get('land_ownership_hectares')} hectares
- Social Category: {profile.get('social_category')}
- Residence Area: {profile.get('residence_area')}
- BPL: {profile.get('is_bpl')}
- Uploaded Supporting Documents in Locker: {", ".join(doc_summary) if doc_summary else "No documents uploaded yet"}
"""

    assessment = invoke_llm_json(user_prompt, system_prompt)

    # Deterministic safety backup if rules_audit is empty
    if not assessment.get("rules_audit"):
        audit_items = []
        has_income_doc = any("income" in (d.get("doc_type", "") + d.get("doc_name", "")).lower() for d in user_docs)
        has_land_doc = any("land" in (d.get("doc_type", "") + d.get("doc_name", "")).lower() for d in user_docs)
        has_vending_doc = any(("vending" in d.get("doc_type", "").lower() or "trade" in d.get("doc_name", "").lower()) for d in user_docs)

        # Age check
        min_age = criteria.get("min_age", 18)
        max_age = criteria.get("max_age", 75)
        user_age = profile.get("age", 30)
        age_passed = min_age <= user_age <= max_age
        audit_items.append({
            "id": 1,
            "rule_text": f"Age must be between {min_age} and {max_age} years",
            "status": "PASSED" if age_passed else "FAILED",
            "citizen_fact": f"Citizen age is {user_age} years",
            "explanation": "Satisfies statutory age bracket." if age_passed else "Outside age requirement."
        })

        # Income check
        max_income = criteria.get("max_annual_income", 300000)
        user_income = profile.get("annual_income", 120000)
        income_passed = (user_income <= max_income if max_income else True) or has_income_doc
        income_fact = f"Citizen annual income is Rs {user_income:,}"
        if has_income_doc:
            income_fact += " (Substantiated by uploaded Income Proof)"
        audit_items.append({
            "id": 2,
            "rule_text": f"Annual household income ceiling of Rs {max_income:,}" if max_income else "No strict income limit",
            "status": "PASSED" if income_passed else "FAILED",
            "citizen_fact": income_fact,
            "explanation": "Income criteria verified and substantiated." if income_passed else "Exceeds income limit."
        })

        # Land check if applicable
        if "land" in json.dumps(criteria).lower():
            land_val = profile.get("land_ownership_hectares", 0)
            land_fact = f"{land_val} hectares"
            if has_land_doc:
                land_fact += " (Substantiated by uploaded Land Records / Khatauni)"
            audit_items.append({
                "id": 3,
                "rule_text": "Landholding ownership verification",
                "status": "PASSED" if (land_val > 0 or has_land_doc) else "SELF_DECLARATION",
                "citizen_fact": land_fact,
                "explanation": "Landholding substantiated by records." if has_land_doc else "Self-declaration acceptable."
            })

        # Key rules as self-declarations
        actionable_declarations = []
        for i, rule in enumerate(key_rules[:3], start=4):
            # If user uploaded documents for this rule, pass it
            rule_lower = rule.lower()
            is_substantiated = False
            if "income" in rule_lower and has_income_doc:
                is_substantiated = True
            elif "land" in rule_lower and has_land_doc:
                is_substantiated = True
            elif ("trade" in rule_lower or "vendor" in rule_lower) and has_vending_doc:
                is_substantiated = True

            audit_items.append({
                "id": i,
                "rule_text": rule,
                "status": "PASSED" if is_substantiated else "SELF_DECLARATION",
                "citizen_fact": "Substantiated by uploaded document in locker" if is_substantiated else "Self-attested statement required",
                "explanation": "Document verified in locker." if is_substantiated else "Please review and confirm this statement."
            })
            if not is_substantiated:
                actionable_declarations.append(rule)

        assessment = {
            "verdict": "ELIGIBLE" if (age_passed and income_passed) else "CONDITIONALLY_ELIGIBLE",
            "score": 96 if (age_passed and income_passed) else 75,
            "summary": "You satisfy the primary demographic and economic qualifications for this welfare initiative.",
            "rules_audit": audit_items,
            "actionable_declarations": actionable_declarations or ["I confirm that the details provided are accurate."]
        }

    return {"eligibility_assessment": assessment}


# ==========================================
# Agent 4: Document Readiness Agent
# ==========================================


def _infer_doc_type_key(req_str: str) -> str:
    """Infers the standard document category key from a scheme requirement string."""
    r = req_str.lower()
    if "aadhaar" in r:
        return "aadhaar"
    if "bank" in r or "passbook" in r:
        return "bank_passbook"
    if "vending" in r or "cov" in r or "trade" in r or "vendor" in r:
        return "vending_certificate"
    if "land" in r or "khasra" in r or "ror" in r or "khatauni" in r or "patta" in r:
        return "land_record"
    if "income" in r or "salary" in r or "bpl" in r:
        return "income_certificate"
    if "caste" in r or "community" in r or "category" in r:
        return "caste_certificate"
    if "ration" in r or "family" in r:
        return "ration_card"
    if "college" in r or "marksheet" in r or "admission" in r or "degree" in r or "diploma" in r:
        return "educational_certificate"
    if "disability" in r or "pwd" in r or "handicap" in r:
        return "disability_certificate"
    return "other"


def _find_matching_user_document(req_str: str, user_docs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Finds a matching user document from the citizen's locker."""
    r = req_str.lower()
    for d in user_docs:
        dt = (d.get("doc_type") or "").lower()
        dn = (d.get("doc_name") or "").lower()

        if "aadhaar" in r and ("aadhaar" in dt or "aadhaar" in dn):
            return d
        if ("bank" in r or "passbook" in r) and ("bank" in dt or "bank" in dn or "passbook" in dt or "passbook" in dn):
            return d
        if ("vending" in r or "cov" in r or "trade" in r) and ("vending" in dt or "vending" in dn or "trade" in dt):
            return d
        if ("land" in r or "khasra" in r or "ror" in r or "khatauni" in r) and ("land" in dt or "land" in dn or "khasra" in dn or "ror" in dn):
            return d
        if ("income" in r or "salary" in r or "affidavit" in r) and ("income" in dt or "income" in dn or "salary" in dn):
            return d
        if ("caste" in r or "category" in r or "community" in r) and ("caste" in dt or "caste" in dn):
            return d
        if ("ration" in r or "family" in r) and ("ration" in dt or "ration" in dn or "family" in dt or "family" in dn):
            return d
        if ("college" in r or "marksheet" in r or "admission" in r or "fee" in r) and ("college" in dt or "admission" in dt or "marksheet" in dn or "fee" in dn):
            return d
        if ("disability" in r or "pwd" in r) and ("disability" in dt or "disability" in dn or "pwd" in dt):
            return d
        # Direct keyword overlap
        if dt and dt != "other" and dt in r:
            return d
    return None


def document_readiness_agent(state: WorkflowState) -> Dict[str, Any]:
    """Cross-references required scheme documents with uploaded user demo documents."""
    logger.info("Executing Agent 4: Document Readiness Agent")
    scheme = state.get("selected_scheme")
    if not scheme and state.get("selected_scheme_id"):
        scheme = get_scheme_by_id(state["selected_scheme_id"])

    user_id = state.get("user_id") or state.get("user_profile", {}).get("id") or 1
    user_docs = get_user_documents(user_id)

    required_docs = scheme.get("required_documents", []) if scheme else []
    if not required_docs:
        required_docs = ["Aadhaar Card (Identity Proof)", "Bank Account Passbook / Statement"]

    doc_status_list = []
    ready_count = 0
    uploaded_count = 0

    for req in required_docs:
        matched = _find_matching_user_document(req, user_docs)
        doc_type_key = _infer_doc_type_key(req)

        if matched:
            raw_status = (matched.get("status") or "UPLOADED").upper()
            doc_id = matched.get("id")
            doc_name = matched.get("doc_name") or req

            if raw_status in ("VERIFIED", "VERIFIED_DEMO"):
                ready_count += 1
                doc_status_list.append({
                    "document_name": req,
                    "status": "READY",
                    "badge": "Verified Demo Document",
                    "notes": "Verified automatically via simulated OCR extraction.",
                    "doc_id": doc_id,
                    "matched_doc_name": doc_name,
                    "doc_type_key": doc_type_key,
                    "is_missing": False
                })
            else:
                # User uploaded document (pending verification)
                uploaded_count += 1
                doc_status_list.append({
                    "document_name": req,
                    "status": "UPLOADED",
                    "badge": "Uploaded (Pending Verification)",
                    "notes": "Document uploaded by citizen; awaiting statutory desk verification.",
                    "doc_id": doc_id,
                    "matched_doc_name": doc_name,
                    "doc_type_key": doc_type_key,
                    "is_missing": False
                })
        else:
            # Unavailable document: Must display status as Missing and provide upload option
            doc_status_list.append({
                "document_name": req,
                "status": "MISSING",
                "badge": "Missing Document",
                "notes": "Required document unavailable in your locker. Click 'Upload Document' to add it.",
                "doc_id": None,
                "matched_doc_name": None,
                "doc_type_key": doc_type_key,
                "is_missing": True
            })

    total_required = max(1, len(required_docs))
    satisfied_count = ready_count + uploaded_count
    missing_count = max(0, total_required - satisfied_count)
    readiness_percentage = round((satisfied_count / total_required) * 100)

    result = {
        "overall_status": "READY_TO_APPLY" if readiness_percentage >= 50 else "DOCUMENTS_NEEDED",
        "ready_count": satisfied_count,
        "verified_count": ready_count,
        "uploaded_count": uploaded_count,
        "missing_count": missing_count,
        "total_required": len(required_docs),
        "readiness_percentage": readiness_percentage,
        "checklist": doc_status_list,
        "can_proceed_demo": True
    }

    return {"document_readiness": result}


# ==========================================
# Agent 5: Application Drafter Agent
# ==========================================

def application_drafter_agent(state: WorkflowState) -> Dict[str, Any]:
    """Compiles complete application draft with formal applicant justification for review."""
    logger.info("Executing Agent 5: Application Drafter Agent")
    scheme = state.get("selected_scheme")
    if not scheme and state.get("selected_scheme_id"):
        scheme = get_scheme_by_id(state["selected_scheme_id"])

    profile = state.get("user_profile", {})
    docs = state.get("document_readiness", {}).get("checklist", [])
    confirmed_rules = state.get("user_confirmed_criteria", [])

    system_prompt = """
You are the Application Drafter Agent for JanSetu.
Your task is to prepare an authoritative, comprehensive formal application draft for the citizen
applying for a government scheme.
The draft must be prepared for the citizen's explicit review before any simulated submission.
Respond in JSON format:
{
  "application_title": "Official Application for <Scheme Name>",
  "target_authority": "Relevant Ministry / Municipal Authority",
  "applicant_summary": {
    "name": "...",
    "category": "...",
    "domicile": "..."
  },
  "statement_of_purpose": "2-3 well-formulated paragraphs explaining citizen's background, livelihood need, and planned utilization of scheme benefits",
  "statutory_declarations": [
    "I hereby confirm...",
    "I declare..."
  ],
  "attached_documents_summary": [
    "Aadhaar Card (Verified Demo)",
    "..."
  ],
  "disclaimer": "This is an AI-generated application draft prepared by JanSetu for demonstration purposes."
}
"""

    ready_doc_names = [d["document_name"] for d in docs if d.get("status") in ("READY", "UPLOADED")]

    user_prompt = f"""
Scheme Name: {scheme.get('name') if scheme else 'Government Welfare Scheme'}
Ministry: {scheme.get('ministry') if scheme else 'Government of India'}
Citizen Profile:
- Full Name: {profile.get('full_name')}
- Occupation: {profile.get('occupation')}
- Annual Income: Rs {profile.get('annual_income')}
- Domicile: {profile.get('district')}, {profile.get('state')}
- Plain Query Need: {state.get('user_query')}
- Confirmed Criteria: {confirmed_rules}
- Ready Documents: {ready_doc_names}
"""

    draft_data = invoke_llm_json(user_prompt, system_prompt)

    # Ensure robust draft structure
    if not draft_data.get("statement_of_purpose"):
        scheme_name = scheme.get("name") if scheme else "Selected Welfare Scheme"
        draft_data = {
            "application_title": f"Application for {scheme_name}",
            "target_authority": scheme.get("ministry", "Concerned Government Department") if scheme else "Government of India",
            "applicant_summary": {
                "name": profile.get("full_name", "Citizen"),
                "occupation": profile.get("occupation", "Worker"),
                "income": f"Rs {profile.get('annual_income', 120000):,}",
                "location": f"{profile.get('district', 'Jaipur')}, {profile.get('state', 'Rajasthan')}"
            },
            "statement_of_purpose": (
                f"I, {profile.get('full_name')}, a resident of {profile.get('district')}, {profile.get('state')}, "
                f"engaged in the occupation of {profile.get('occupation')}, respectfully submit this application "
                f"for assistance under {scheme_name}. My household annual income is Rs {profile.get('annual_income'):,}, "
                f"falling squarely within the targeted socio-economic eligibility criteria. "
                f"The assistance will be diligently utilized to sustain my livelihood and provide essential welfare security for my family."
            ),
            "statutory_declarations": [
                "I affirm that all demographic and financial information submitted herein is true and accurate.",
                "I have verified that I meet the eligibility conditions set forth in the scheme operational guidelines.",
                "I consent to simulated verification of my demo documents under the JanSetu demonstration protocol."
            ],
            "attached_documents_summary": ready_doc_names or ["Aadhaar Card (Demo)", "Bank Passbook (Demo)"],
            "disclaimer": "This is an AI-generated application draft prepared by JanSetu for hackathon prototype demonstration."
        }

    return {"application_draft": draft_data}


# ==========================================
# LangGraph Workflow Graph Assembly
# ==========================================

def build_workflow_graph() -> StateGraph:
    """Assembles the LangGraph StateGraph connecting the 5 workflow agents."""
    graph = StateGraph(WorkflowState)

    # Add agent nodes
    graph.add_node("need_intake", need_intake_agent)
    graph.add_node("scheme_matcher", scheme_matcher_agent)
    graph.add_node("eligibility_assessor", eligibility_assessor_agent)
    graph.add_node("document_readiness", document_readiness_agent)
    graph.add_node("application_drafter", application_drafter_agent)

    # Define edges: Linear orchestration pipeline
    graph.set_entry_point("need_intake")
    graph.add_edge("need_intake", "scheme_matcher")
    graph.add_edge("scheme_matcher", "eligibility_assessor")
    graph.add_edge("eligibility_assessor", "document_readiness")
    graph.add_edge("document_readiness", "application_drafter")
    graph.add_edge("application_drafter", END)

    return graph.compile()


# Compiled workflow runner instance
workflow_runner = build_workflow_graph()


def run_full_workflow(
    user_id: int,
    user_query: str,
    selected_scheme_id: Optional[int] = None,
    user_confirmed_criteria: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Executes the full LangGraph 5-agent pipeline."""
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")

    selected_scheme = get_scheme_by_id(selected_scheme_id) if selected_scheme_id else None

    initial_state: WorkflowState = {
        "user_id": user_id,
        "user_profile": user,
        "user_query": user_query,
        "selected_scheme_id": selected_scheme_id,
        "selected_scheme": selected_scheme,
        "intake_result": None,
        "recommendations": None,
        "eligibility_assessment": None,
        "document_readiness": None,
        "application_draft": None,
        "user_confirmed_criteria": user_confirmed_criteria or [],
        "error": None
    }

    final_state = workflow_runner.invoke(initial_state)
    return final_state
