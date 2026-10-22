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
    candidate_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]
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


def _parse_kb_schemes(system_prompt: Optional[str]) -> List[Dict[str, Any]]:
    """Extracts structured schemes from system prompt knowledge base block."""
    schemes = []
    if not system_prompt or "[Official Knowledge Base" not in system_prompt:
        return schemes
    try:
        kb_text = system_prompt.split("[Official Knowledge Base")[1]
        blocks = kb_text.split("---")
        for b in blocks:
            b = b.strip()
            if not b or "Scheme:" not in b:
                continue
            name_m = re.search(r"Scheme:\s*([^\n\r]+)", b)
            if not name_m:
                continue
            full_name = name_m.group(1).strip()
            code_m = re.search(r"\(([^)]+)\)$", full_name)
            code = code_m.group(1).strip() if code_m else ""
            name = full_name[:code_m.start()].strip() if code_m else full_name

            min_m = re.search(r"Ministry:\s*([^\n\r]+)", b)
            cat_m = re.search(r"Category:\s*([^\n\r]+)", b)
            ben_m = re.search(r"Benefits:\s*([^\n\r]+)", b)
            elig_m = re.search(r"Eligibility:\s*([^\n\r]+)", b)
            docs_m = re.search(r"Required Documents:\s*([^\n\r]+)", b)
            link_m = re.search(r"Official Link:\s*([^\n\r]+)", b)

            elig_list = []
            if elig_m:
                raw_el = elig_m.group(1).strip()
                try:
                    elig_list = json.loads(raw_el.replace("'", '"'))
                except Exception:
                    raw_el = raw_el.strip("[]")
                    elig_list = [x.strip(" '\"") for x in raw_el.split(",") if x.strip(" '\"")]

            docs_list = []
            if docs_m:
                raw_dc = docs_m.group(1).strip()
                try:
                    docs_list = json.loads(raw_dc.replace("'", '"'))
                except Exception:
                    raw_dc = raw_dc.strip("[]")
                    docs_list = [x.strip(" '\"") for x in raw_dc.split(",") if x.strip(" '\"")]

            schemes.append({
                "name": name,
                "code": code,
                "ministry": min_m.group(1).strip() if min_m else "Government of India",
                "category": cat_m.group(1).strip() if cat_m else "Citizen Welfare",
                "benefits": ben_m.group(1).strip() if ben_m else "",
                "eligibility": [e for e in elig_list if e],
                "required_documents": [d for d in docs_list if d],
                "official_url": link_m.group(1).strip() if link_m else "https://www.myscheme.gov.in"
            })
    except Exception as e:
        logger.warning(f"Error parsing KB schemes: {e}")
    return schemes


def _simulate_reasoning(prompt: str, system_prompt: Optional[str], json_mode: bool) -> str:
    """Provides high-quality realistic agent responses when API keys are not supplied."""
    p_lower = prompt.lower()

    # Chatbot queries (JanSetu Mitra)
    if "mitra" in (system_prompt or "").lower() or "chatbot" in p_lower or "ask" in p_lower:
        # Extract citizen's current message
        m_msg = re.search(r"Citizen's Current Message:\s*\n?(.*?)(?:\n\[|$)", prompt, re.DOTALL)
        citizen_msg = m_msg.group(1).strip() if m_msg else prompt.strip()
        c_lower = citizen_msg.lower()

        # Check for simple greeting
        if re.search(r"^(hi|hello|hey|namaste|pranam|good\s*(morning|afternoon|evening)|who are you|help|start)\b", c_lower) and len(c_lower.split()) <= 4:
            return (
                "Namaste! I am JanSetu Mitra (जनसेतु मित्र), your personal AI Welfare Advisor.\n\n"
                "I can assist you with:\n"
                "• Scheme Discovery: Finding government schemes suited to your profile and need.\n"
                "• Eligibility Criteria: Explaining age, income ceiling, and category requirements.\n"
                "• Required Documents: Identifying all mandatory certificates and proofs.\n"
                "• Application Process: Official portals, application forms, and guided workflows.\n\n"
                "What can I help you with today? Feel free to ask about scholarships, health insurance (Ayushman Bharat), housing subsidies (PMAY), vendor/business loans (PM SVANidhi/Mudra), pensions, or farming assistance!"
            )

        # Check for pet / domestic animal queries (dog, cat, pet)
        if any(w in c_lower for w in ["dog", "dogs", "cat", "cats", "pet", "pets", "puppy", "puppies", "kitten", "kittens"]):
            return (
                "Namaste! Government welfare schemes in India are designed for citizen welfare "
                "(such as scholarships, healthcare, housing, pensions, and livelihood loans) and agricultural livestock "
                "(such as dairy cattle, buffaloes, sheep, poultry, and fisheries).\n\n"
                "There are currently no Central or State government subsidy or welfare schemes for domestic household pets such as dogs or cats.\n\n"
                "However, if you are looking for agricultural animal husbandry or dairy development schemes, "
                "programs like the Rashtriya Gokul Mission and National Livestock Mission provide capital subsidies. "
                "For citizen support, you can explore student scholarships, Ayushman Bharat health coverage, PMAY housing assistance, or PM SVANidhi loans!"
            )

        kb_schemes = _parse_kb_schemes(system_prompt)

        # If schemes were retrieved from vector search
        if kb_schemes:
            s1 = kb_schemes[0]
            s_name = s1["name"]
            s_code = f" ({s1['code']})" if s1.get("code") else ""

            # Check intent: Documents
            if any(w in c_lower for w in ["document", "documents", "paper", "papers", "proof", "certificate", "certificates", "what docs", "docs", "what to bring", "upload"]):
                docs = s1.get("required_documents") or ["Aadhaar Card", "Bank Account Passbook", "Income Certificate"]
                docs_text = "\n".join(f"• {d}" for d in docs)
                return (
                    f"To apply for {s_name}{s_code}, please prepare the following mandatory documents:\n\n"
                    f"{docs_text}\n\n"
                    f"Checklist Guidance: Ensure your bank account is linked with your Aadhaar for direct benefit transfer (DBT). "
                    f"You can also use JanSetu's Document Readiness Agent (Stage 4) to upload and automatically verify these documents!"
                )

            # Check intent: Eligibility
            if any(w in c_lower for w in ["eligible", "eligibility", "qualify", "criteria", "rule", "rules", "who can apply", "can i apply", "income limit", "age limit", "requirement"]):
                rules = s1.get("eligibility") or ["Applicant must satisfy statutory demographic and income ceiling requirements."]
                rules_text = "\n".join(f"• {r}" for r in rules)
                return (
                    f"Statutory eligibility criteria for {s_name}{s_code}:\n\n"
                    f"{rules_text}\n\n"
                    f"• Category / Sector: {s1.get('category')}\n"
                    f"• Ministry: {s1.get('ministry')}\n\n"
                    f"You can also run our Eligibility Assessor Agent (Stage 3) in the AI Assistant to audit your profile with automated rule checks!"
                )

            # Check intent: Application procedure / How to apply
            if any(w in c_lower for w in ["how to apply", "how do i apply", "apply", "application", "procedure", "process", "register", "registration", "portal", "website", "link"]):
                portal = s1.get("official_url") or "https://www.myscheme.gov.in"
                docs_brief = ", ".join(s1.get("required_documents", ["Aadhaar Card", "Bank Passbook"])[:3])
                return (
                    f"Application procedure for {s_name}{s_code}:\n\n"
                    f"1. Assemble Required Proofs: Gather your {docs_brief}.\n"
                    f"2. Official Portal: Access the designated portal at {portal} or visit your nearest Common Service Centre (CSC) / Municipal Office.\n"
                    f"3. Submit Application: Fill in the citizen details, upload documents, and note down your reference number.\n\n"
                    f"JanSetu Drafter: You can use our Application Drafter Agent (Stage 5) to automatically generate a pre-filled, compliant official application draft!"
                )

            # Check intent: Benefits / Subsidy / Money amount
            if any(w in c_lower for w in ["benefit", "benefits", "amount", "how much", "subsidy", "money", "grant", "financial help", "payment", "paisa"]):
                reply = (
                    f"Benefits provided under {s_name}{s_code}:\n\n"
                    f"• Core Benefit: {s1.get('benefits')}\n"
                    f"• Implementing Ministry: {s1.get('ministry')}\n"
                    f"• Target Sector: {s1.get('category')}\n\n"
                )
                rel_alts = [s for s in kb_schemes[1:2] if s.get("category") == s1.get("category")]
                if rel_alts:
                    s2 = rel_alts[0]
                    reply += f"Related Initiative: {s2['name']} also provides: {s2.get('benefits')[:120]}...\n\n"
                reply += "Would you like me to explain the eligibility rules or mandatory documents for this scheme?"
                return reply

            # General scheme response
            reply = (
                f"Namaste! Regarding your query on \"{citizen_msg}\", here is the best matching government welfare scheme:\n\n"
                f"Scheme: {s_name}{s_code}\n"
                f"• Ministry / Sector: {s1.get('ministry')} ({s1.get('category')})\n"
                f"• Key Benefits: {s1.get('benefits')}\n"
            )
            if s1.get("eligibility"):
                reply += f"• Eligibility: {'; '.join(s1['eligibility'][:2])}\n"
            if s1.get("required_documents"):
                reply += f"• Key Documents: {', '.join(s1['required_documents'][:3])}\n"

            # Filter relevant alternatives (only same category)
            rel_alts = [s for s in kb_schemes[1:3] if s.get("category") == s1.get("category")]
            if rel_alts:
                reply += "\nRelated Welfare Initiatives:\n"
                for s_alt in rel_alts:
                    reply += f"• {s_alt['name']}: {s_alt.get('benefits')[:90]}...\n"

            reply += (
                f"\nOfficial Portal: {s1.get('official_url', 'https://www.myscheme.gov.in')}\n"
                f"Next Steps: You can also use our AI Assistant (Stages 1-5) to audit your eligibility and generate an official application draft."
            )
            return reply

        # Fallback if no schemes in knowledge base
        return (
            f"Namaste! Regarding \"{citizen_msg}\", JanSetu connects you to over 80+ Central and State welfare initiatives. "
            f"Please mention your specific sector (e.g., student scholarship, farmer financial assistance, street vendor loan, health insurance, or pension) "
            f"so I can provide precise eligibility rules and document requirements!"
        )

    # Need Intake Agent
    if "intake" in (system_prompt or "").lower() or "need" in p_lower:
        if json_mode:
            # Extract citizen query from prompt
            m = re.search(r'Citizen\'s Plain Language Query:\s*\n?"([^"\n\r]+)"', prompt, re.DOTALL)
            citizen_query = m.group(1).strip() if m else ""
            if not citizen_query:
                m2 = re.search(r'"([^"\n\r]{3,120})"', prompt)
                citizen_query = m2.group(1).strip() if m2 else prompt[:80]

            q_lower = citizen_query.lower()

            if any(w in q_lower for w in ["scholarship", "college", "school", "education", "student", "study", "fee", "degree", "coaching", "tuition"]):
                category = "Education & Learning"
                intent = "Scholarship and Education Financial Assistance"
                search_q = f"scholarship college university education student fee aid {citizen_query}"
            elif any(w in q_lower for w in ["health", "hospital", "medical", "treatment", "ayushman", "doctor", "medicine", "surgery", "disease", "arogya", "illness", "swasth"]):
                category = "Health & Wellness"
                intent = "Medical Insurance and Healthcare Grant"
                search_q = f"health insurance medical treatment hospital cashless treatment coverage {citizen_query}"
            elif any(w in q_lower for w in ["house", "housing", "awas", "pucca", "home", "shelter", "roof", "makaan", "colony"]):
                category = "Housing & Shelter"
                intent = "Housing Grant and Pucca House Construction Subsidy"
                search_q = f"housing subsidy pucca house construction assistance gramin urban awas {citizen_query}"
            elif any(w in q_lower for w in ["vendor", "shop", "street", "cart", "thela", "hawker", "svanidhi", "working capital", "re-employment", "re-start"]):
                category = "Micro-Enterprise"
                intent = "Working Capital Loan and Collateral-Free Credit"
                search_q = f"street vendor working capital loan collateral free pm svanidhi micro credit {citizen_query}"
            elif any(w in q_lower for w in ["pension", "old age", "elderly", "senior", "widow", "vridha", "divyang", "disability", "handicap", "pensioner"]):
                category = "Social Security"
                intent = "Monthly Social Security Pension and Disability Allowance"
                search_q = f"social security pension monthly financial support disability old age widow {citizen_query}"
            elif any(w in q_lower for w in ["farmer", "farm", "crop", "kisan", "tractor", "seed", "fertilizer", "irrigation", "agriculture", "fasal", "dbt"]):
                category = "Agriculture"
                intent = "Direct Farm Income Support and Crop Protection"
                search_q = f"farmer financial assistance direct benefit crop income support pm kisan {citizen_query}"
            elif any(w in q_lower for w in ["women", "girl", "daughter", "maternity", "sukanya", "beti", "mahila", "shg", "self help"]):
                category = "Social Welfare"
                intent = "Women and Child Welfare Grant"
                search_q = f"women welfare empowerment financial grant girl child education {citizen_query}"
            elif any(w in q_lower for w in ["loan", "credit", "mudra", "subsidy", "finance", "business"]):
                category = "Micro-Enterprise"
                intent = "Business Credit and Entrepreneurship Subsidy"
                search_q = f"collateral free business loan credit subsidy mudra {citizen_query}"
            else:
                category = "General Welfare"
                intent = "Government Welfare Assistance"
                search_q = citizen_query

            return json.dumps({
                "need_summary": f"Identified {intent.lower()} requirement based on your request.",
                "extracted_need": citizen_query,
                "identified_category": category,
                "detected_intent": intent,
                "extracted_entities": {
                    "assistance_type": intent,
                    "target_sector": category,
                    "priority": "High"
                },
                "semantic_search_query": search_q
            })

    # Scheme Matcher Agent
    if "matcher" in (system_prompt or "").lower() or ("candidate" in (system_prompt or "").lower() and "scheme" in (system_prompt or "").lower()):
        if json_mode:
            ids = [int(x) for x in re.findall(r'"scheme_id":\s*(\d+)', prompt)]
            if not ids:
                ids = [1, 2, 3]
            recs = []
            for i, sid in enumerate(ids[:3]):
                recs.append({
                    "scheme_id": sid,
                    "code": f"SCHEME-{sid}",
                    "name": f"Scheme #{sid}",
                    "match_score": 96 - (i * 4),
                    "match_rationale": "High semantic affinity with citizen profile, income tier, and livelihood category.",
                    "key_highlight": "Subsidized interest, collateral-free credit, and direct bank disbursement."
                })
            return json.dumps({"recommendations": recs})

    # Eligibility Assessor Agent
    if "eligibility" in (system_prompt or "").lower():
        if json_mode:
            return json.dumps({
                "verdict": "ELIGIBLE",
                "overall_verdict": "ELIGIBLE",
                "score": 94,
                "eligibility_score": 94,
                "summary": "Citizen satisfies core statutory eligibility requirements. Personal self-declaration requires confirmation.",
                "rules_audit": [
                    {"id": 1, "rule_text": "Age within eligible statutory range (18-65 years)", "status": "PASSED", "citizen_fact": "Applicant meets the statutory age bracket.", "explanation": "Demographic validation passed."},
                    {"id": 2, "rule_text": "Annual household income within prescribed ceiling", "status": "PASSED", "citizen_fact": "Income within scheme ceiling.", "explanation": "Economic requirement fully satisfied."},
                    {"id": 3, "rule_text": "Livelihood sector and occupational category", "status": "PASSED", "citizen_fact": "Active occupational profile aligns with target demographic.", "explanation": "Domain eligibility confirmed."},
                    {"id": 4, "rule_text": "No active institutional loan defaults", "status": "SELF_DECLARATION", "citizen_fact": "Pending self-affirmation.", "explanation": "Please confirm no active defaults with commercial or scheduled banks."}
                ],
                "actionable_declarations": [
                    "I declare that I do not have any non-performing or defaulted institutional loans.",
                    "I confirm that all submitted family income and livelihood statements are genuine and correct."
                ]
            })

    # Document Readiness Agent
    if "document" in (system_prompt or "").lower():
        if json_mode:
            return json.dumps({
                "overall_status": "READY_TO_APPLY",
                "readiness_verdict": "READY_FOR_APPLICATION",
                "ready_count": 3,
                "missing_count": 0,
                "total_required": 3,
                "readiness_percentage": 100,
                "checklist": [
                    {"document_name": "Aadhaar Card", "status": "READY", "badge": "Verified Demo Document", "notes": "Identity and masked biometric ID verified from demo records."},
                    {"document_name": "Active Bank Passbook", "status": "READY", "badge": "Verified Demo Document", "notes": "Aadhaar-seeded bank account found with DBT linkage active."},
                    {"document_name": "Vending / Occupational Certificate", "status": "READY", "badge": "Verified Demo Document", "notes": "Local municipal authority credential verified."}
                ]
            })

    # Application Drafter Agent
    if "draft" in (system_prompt or "").lower():
        if json_mode:
            return json.dumps({
                "application_title": "Official Application for Welfare Scheme",
                "target_authority": "Ministry of Housing and Urban Affairs / State Welfare Department",
                "applicant_summary": {
                    "name": "Citizen Beneficiary",
                    "occupation": "Street Vendor / Self-Employed",
                    "income": "Rs 1,20,000",
                    "location": "Jaipur, Rajasthan"
                },
                "statement_of_purpose": "The applicant is a genuine citizen requiring welfare assistance in accordance with prescribed guidelines to expand their livelihood.",
                "statutory_declarations": [
                    "I affirm that all demographic and financial information submitted herein is true and accurate.",
                    "I have verified that I meet the eligibility conditions set forth in scheme guidelines."
                ],
                "attached_documents_summary": ["Aadhaar Proof (Demo)", "Bank Account Passbook (Demo)", "Occupational Certificate (Demo)"],
                "disclaimer": "This application draft has been compiled by the JanSetu AI Agentic Workforce for prototype demonstration only."
            })

    # Default JSON fallback
    if json_mode:
        return json.dumps({"status": "SUCCESS", "message": "Processed successfully by JanSetu engine."})

    return "Processed successfully by JanSetu engine."
