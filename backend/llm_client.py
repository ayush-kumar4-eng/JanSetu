"""
JanSetu LLM Orchestration Client
Primary LLM: Groq (Llama-3.3-70b / Llama-3.1-8b)
Fallback LLM: Google Gemini (gemini-2.0-flash / gemini-1.5-flash)
Graceful Mock Engine: Runs intelligent local heuristic responses if keys are omitted.
"""

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional
from backend.config import GROQ_API_KEY, GEMINI_API_KEY

logger = logging.getLogger("JanSetu.LLMClient")


def _call_groq(prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
    """Invokes Groq via official groq package or requests."""
    # pyrefly: ignore[missing-import]
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY, max_retries=1)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Try active high-performance models on this Groq account
    candidate_models = ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
    last_err = None

    for model_name in candidate_models:
        try:
            kwargs = {
                "model": model_name,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 1500,
                "timeout": 10.0,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            chat_completion = client.chat.completions.create(**kwargs)
            return chat_completion.choices[0].message.content or ""
        except Exception as e:
            last_err = e
            continue

    raise last_err or RuntimeError("No candidate Groq model succeeded")


def _call_gemini(prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
    """Invokes Google Gemini as fallback."""
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        full_content = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        if json_mode:
            full_content += "\n\nCRITICAL: Respond ONLY with valid JSON with no markdown backticks or commentary."
        for g_model in ["gemini-3.8-flash", "gemini-2.5-flash", "models/gemini-3.8-flash"]:
            try:
                response = client.models.generate_content(
                    model=g_model,
                    contents=full_content,
                )
                if response and response.text:
                    return response.text.strip()
            except Exception:
                continue
        return ""
    except Exception as e:
        logger.warning(f"Gemini client invocation failed: {e}")
        return ""


def _clean_json_string(text: str) -> str:
    """Strips markdown code fences and whitespace from json string."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def invoke_llm(prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
    """
    Executes prompt with primary LLM (Groq), cascading to Gemini fallback,
    and finally intelligent rule-based simulation if keys are unavailable.
    """
    # 1. Try Groq
    if GROQ_API_KEY and not GROQ_API_KEY.startswith("your_"):
        try:
            logger.info("Attempting inference via primary LLM: Groq")
            return _call_groq(prompt, system_prompt, json_mode)
        except Exception as e:
            logger.warning(f"Groq API call failed: {e}. Trying Gemini fallback...")

    # 2. Try Gemini
    if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("your_"):
        try:
            logger.info("Attempting inference via fallback LLM: Google Gemini")
            return _call_gemini(prompt, system_prompt, json_mode)
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}. Triggering intelligent fallback engine...")

    # 3. Intelligent Local Simulation Engine (ensures robust hackathon zero-crash behavior)
    logger.info("Using JanSetu Built-in Intelligent Reasoning Engine")
    return _simulate_reasoning(prompt, system_prompt, json_mode)


def invoke_llm_json(prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
    """Invokes LLM and safely parses output as JSON dict."""
    raw = invoke_llm(prompt, system_prompt, json_mode=True)
    cleaned = _clean_json_string(raw)
    try:
        return json.loads(cleaned)
    except Exception as e:
        logger.warning(f"JSON parsing error: {e}. Attempting regex extraction.")
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
        return {"raw_response": raw, "error": "Failed to parse JSON"}


def _simulate_reasoning(prompt: str, system_prompt: Optional[str], json_mode: bool) -> str:
    """Provides high-quality realistic agent responses when API keys are not supplied."""
    p_lower = prompt.lower()

    # Chatbot queries
    if "mitra" in (system_prompt or "").lower() or "chatbot" in p_lower or "ask" in p_lower:
        if "svanidhi" in p_lower or "vendor" in p_lower or "loan" in p_lower:
            return (
                "Namaste! **PM SVANidhi** provides collateral-free working capital loans of up to ₹50,000 for urban street vendors. "
                "The 1st tranche is ₹10,000, 2nd tranche ₹20,000, and 3rd tranche ₹50,000 with a 7% interest subsidy! "
                "You only need your Aadhaar, Bank Passbook, and Certificate of Vending (or Letter of Recommendation from your municipal council)."
            )
        elif "kisan" in p_lower or "farmer" in p_lower:
            return (
                "Namaste! **PM-KISAN** grants ₹6,000 per year directly to cultivable landholding farmer families in 3 equal installments of ₹2,000. "
                "Key documents required: Aadhaar Card, Land Records (Khatauni/Khasra), and Aadhaar-seeded Bank Passbook."
            )
        elif "housing" in p_lower or "awas" in p_lower or "pmay" in p_lower:
            return (
                "Under **PMAY-Urban**, eligible EWS and LIG families receive up to ₹2.67 Lakh subsidy or financial grant to construct or purchase a pucca home. "
                "The primary rule is that the family must not own a pucca house anywhere in India."
            )
        else:
            return (
                "Namaste! I am **JanSetu Mitra**, your AI citizen welfare advisor. "
                "I can help you explore over 700+ Central and State welfare schemes, check eligibility rules, list mandatory documents, "
                "and explain application procedures. Tell me about your occupation, family income, or specific financial need!"
            )

    # Need Intake Agent
    if "intake" in (system_prompt or "").lower() or "need" in p_lower:
        if json_mode:
            return json.dumps({
                "need_summary": "Assistance identified based on citizen declaration.",
                "identified_category": "Micro-Enterprise" if "vendor" in p_lower or "loan" in p_lower or "shop" in p_lower else ("Agriculture" if "farm" in p_lower or "crop" in p_lower else "Social Security"),
                "detected_intent": "Financial support / loan / grant",
                "extracted_entities": {
                    "assistance_type": "Working capital credit or direct benefit",
                    "priority": "High"
                }
            })

    # Eligibility Assessor Agent
    if "eligibility" in (system_prompt or "").lower():
        if json_mode:
            return json.dumps({
                "overall_verdict": "ELIGIBLE",
                "eligibility_score": 92,
                "summary": "Citizen satisfies core statutory eligibility requirements. One self-declaration item requires citizen confirmation.",
                "checklist": [
                    {"criterion": "Age within eligible range (18-65 years)", "status": "PASSED", "details": "Applicant meets the age requirement."},
                    {"criterion": "Annual household income within ceiling", "status": "PASSED", "details": "Income is within prescribed limits for this scheme."},
                    {"criterion": "Occupation and operational domain", "status": "PASSED", "details": "Citizen's livelihood aligns with targeted beneficiary demographic."},
                    {"criterion": "No active institutional loan defaults", "status": "SELF_DECLARATION", "details": "Please confirm you have no unpaid defaults with public sector banks."}
                ]
            })

    # Document Readiness Agent
    if "document" in (system_prompt or "").lower():
        if json_mode:
            return json.dumps({
                "readiness_verdict": "READY_FOR_APPLICATION",
                "ready_count": 3,
                "missing_count": 0,
                "documents": [
                    {"name": "Aadhaar Card", "status": "READY", "notes": "Identity and masked biometric ID verified from demo records."},
                    {"name": "Active Bank Passbook", "status": "READY", "notes": "Aadhaar-seeded bank account found with DBT linkage active."},
                    {"name": "Vending / Occupational Certificate", "status": "READY", "notes": "Local municipal authority credential verified."}
                ]
            })

    # Application Drafter Agent
    if "draft" in (system_prompt or "").lower():
        if json_mode:
            return json.dumps({
                "draft_title": "Official Welfare Assistance Application Form (JanSetu Demonstration)",
                "applicant_name": "Citizen Beneficiary",
                "scheme_target": "Government Welfare Scheme",
                "statement_of_need": "The applicant is a genuine citizen requiring welfare assistance in accordance with prescribed guidelines.",
                "eligibility_affirmation": "All statutory criteria including income threshold, occupational eligibility, and residency requirements have been cross-verified.",
                "uploaded_credentials": ["Aadhaar Proof", "Bank Account Passbook", "Occupational Certificate"],
                "disclaimer": "This application draft has been compiled by the JanSetu AI Agentic Workforce for prototype demonstration only."
            })

    # Default JSON fallback
    if json_mode:
        return json.dumps({"status": "SUCCESS", "message": "Processed successfully by JanSetu engine."})

    return "Processed successfully by JanSetu engine."
