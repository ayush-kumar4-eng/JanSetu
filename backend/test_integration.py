"""
JanSetu Comprehensive Integration and Workflow Verification Test
Tests API configurations, database operations, Qdrant search, LLM responses, and 5-agent workflow.
"""

import sys
import json
import time
from pathlib import Path

# Fix Windows cp1252 print encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import get_all_schemes, get_user_by_id

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("      JanSetu Integration & Workflow Verification")
    print("=" * 60)

    # 1. Health Endpoint
    print("\n[Test 1] Health Endpoint Check...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print(f" [PASS] Status: {health_data['status']}, Service: {health_data['service']}")

    # 2. Users & Citizen Personas
    print("\n[Test 2] Users & Citizen Personas Check...")
    res = client.get("/api/users")
    assert res.status_code == 200, f"Users fetch failed: {res.text}"
    users = res.json().get("users", [])
    assert len(users) >= 1, "No users found in database"
    print(f" [PASS] Found {len(users)} citizen personas. Active demo user: {users[0]['full_name']} ({users[0]['occupation']})")

    # 3. Scheme Catalog & Categories
    print("\n[Test 3] Scheme Catalog & Categories Check...")
    res = client.get("/api/schemes")
    assert res.status_code == 200, f"Schemes list failed: {res.text}"
    schemes_data = res.json()
    scheme_count = schemes_data.get("count", 0)
    assert scheme_count >= 80, f"Expected at least 80 schemes, got {scheme_count}"
    print(f" [PASS] Schemes in Catalog: {scheme_count}")

    res_cat = client.get("/api/schemes/categories")
    assert res_cat.status_code == 200
    categories = res_cat.json().get("categories", [])
    print(f" [PASS] Unique Scheme Categories: {len(categories)} ({', '.join(categories[:4])}...)")

    # 4. Semantic Search (Qdrant)
    print("\n[Test 4] Qdrant Semantic Vector Search...")
    sample_query = "working capital loan for street vendors"
    res_search = client.get(f"/api/schemes/search?q={sample_query}&limit=3")
    assert res_search.status_code == 200, f"Search failed: {res_search.text}"
    search_results = res_search.json().get("results", [])
    assert len(search_results) > 0, "No search results returned from Qdrant"
    print(f" [PASS] Top Qdrant match: '{search_results[0]['name']}' (Score: {search_results[0]['match_percentage']})")
    print(f"        Official Portal: {search_results[0].get('official_url')}")

    # 5. Agent 1 & 2: Need Intake & Scheme Matcher
    print("\n[Test 5] Stage 1 & 2 Workflow: Need Intake & Matcher Agents...")
    payload_match = {
        "user_id": 1,
        "user_query": "I run a small tea stall in Jaipur and need 20000 rupees to buy raw materials and utensils without mortgaging property."
    }
    res_match = client.post("/api/workflow/intake-and-match", json=payload_match)
    assert res_match.status_code == 200, f"Intake & Match failed: {res_match.text}"
    match_data = res_match.json()
    recs = match_data.get("recommendations", [])
    assert len(recs) >= 1, "Expected recommendations"
    selected_scheme = recs[0]
    print(f" [PASS] Need Intake Summary: {match_data.get('intake_analysis', {}).get('need_summary')}")
    print(f" [PASS] Top Recommendation: {selected_scheme['name']} (Score: {selected_scheme.get('match_percentage')})")
    print(f"        Rationale: {selected_scheme.get('match_rationale', '')[:80]}...")

    # 6. Agent 3: Eligibility Assessor
    time.sleep(1.0)
    print("\n[Test 6] Stage 3 Workflow: Eligibility Assessor Agent...")
    payload_elig = {
        "user_id": 1,
        "scheme_id": selected_scheme["id"]
    }
    res_elig = client.post("/api/workflow/audit-eligibility", json=payload_elig)
    assert res_elig.status_code == 200, f"Eligibility audit failed: {res_elig.text}"
    elig_data = res_elig.json().get("eligibility", {})
    print(f" [PASS] Verdict: {elig_data.get('verdict')} (Score: {elig_data.get('score')}%)")
    print(f"        Rules audited: {len(elig_data.get('rules_audit', []))} criteria evaluated")

    # 7. Agent 4: Document Readiness
    print("\n[Test 7] Stage 4 Workflow: Document Readiness Agent...")
    payload_doc = {
        "user_id": 1,
        "scheme_id": selected_scheme["id"]
    }
    res_doc = client.post("/api/workflow/audit-documents", json=payload_doc)
    assert res_doc.status_code == 200, f"Document audit failed: {res_doc.text}"
    doc_data = res_doc.json().get("document_readiness", {})
    print(f" [PASS] Readiness Status: {doc_data.get('status')} ({doc_data.get('ready_count')} Ready / {doc_data.get('missing_count')} Missing)")

    # 8. Agent 5: Application Drafter
    time.sleep(1.0)
    print("\n[Test 8] Stage 5 Workflow: Application Drafter Agent...")
    payload_draft = {
        "user_id": 1,
        "scheme_id": selected_scheme["id"],
        "user_query": payload_match["user_query"],
        "confirmed_criteria": ["Applicant is actively engaged in urban street vending."]
    }
    res_draft = client.post("/api/workflow/generate-draft", json=payload_draft)
    assert res_draft.status_code == 200, f"Draft generation failed: {res_draft.text}"
    draft_data = res_draft.json().get("application_draft", {})
    summary_text = draft_data.get("statement_of_purpose") or draft_data.get("application_title", "")
    print(f" [PASS] Generated Application Title: {draft_data.get('application_title')}")
    print(f"        Purpose Summary: {summary_text[:80]}...")

    # 9. Simulated Submission & Safety Gate
    print("\n[Test 9] Stage 6 Workflow: Simulated Submission (Safety Guardrail Test)...")
    # Verify rejection without explicit approval
    fail_payload = {
        "user_id": 1,
        "scheme_id": selected_scheme["id"],
        "explicit_approval": False,
        "applicant_data": {"name": "Ramesh"},
        "draft_summary": "Test"
    }
    res_fail = client.post("/api/workflow/submit-simulated", json=fail_payload)
    assert res_fail.status_code == 400, "Safety violation: Submission allowed without explicit approval"
    print(" [PASS] Safety Guardrail verified: submission blocked without explicit user approval.")

    # Successful simulated submission
    submit_payload = {
        "user_id": 1,
        "scheme_id": selected_scheme["id"],
        "explicit_approval": True,
        "applicant_data": draft_data.get("applicant_summary", {"name": "Ramesh Kumar"}),
        "eligibility_answers": [{"rule": "Street vending", "status": "CONFIRMED"}],
        "draft_summary": summary_text,
        "notes": "Automated verification test run"
    }
    res_sub = client.post("/api/workflow/submit-simulated", json=submit_payload)
    assert res_sub.status_code == 200, f"Submission failed: {res_sub.text}"
    sub_data = res_sub.json()
    ref_no = sub_data.get("reference_no")
    print(f" [PASS] Simulated Application Created: Ref #{ref_no}")
    print(f"        Disclaimer: {sub_data.get('disclaimer')}")

    # 10. Application Tracking
    print("\n[Test 10] Application History & Tracking Timeline...")
    res_apps = client.get("/api/applications/user/1")
    assert res_apps.status_code == 200
    user_apps = res_apps.json().get("applications", [])
    assert len(user_apps) >= 1
    print(f" [PASS] User has {len(user_apps)} active application records in tracking system.")

    res_single = client.get(f"/api/applications/ref/{ref_no}")
    assert res_single.status_code == 200
    single_app = res_single.json().get("application", {})
    tracking_steps = single_app.get("tracking_history", [])
    print(f" [PASS] Tracking history milestones: {len(tracking_steps)} steps logged.")

    # 11. Search-Only Chatbot (JanSetu Mitra)
    time.sleep(1.0)
    print("\n[Test 11] Search-Only Chatbot (JanSetu Mitra)...")
    chat_payload = {
        "session_id": "test_session_verification_101",
        "message": "What is PM Kisan and what are the required documents for it?",
        "user_id": 1
    }
    res_chat = client.post("/api/chat", json=chat_payload)
    assert res_chat.status_code == 200, f"Chat failed: {res_chat.text}"
    chat_data = res_chat.json()
    reply = chat_data.get("reply", "")
    assert len(reply) > 20, "Chatbot reply was empty or too short"
    print(f" [PASS] JanSetu Mitra Response ({len(reply)} chars):")
    print(f"        '{reply[:120]}...'")

    # 12. Direct Notifications Endpoint
    print("\n[Test 12] Direct Notifications Endpoint Check (/api/notifications/user/1)...")
    res_notif = client.get("/api/notifications/user/1")
    assert res_notif.status_code == 200, f"Notifications failed: {res_notif.text}"
    notif_data = res_notif.json().get("notifications", [])
    print(f" [PASS] Notifications retrieved: {len(notif_data)} citizen alerts active.")

    # 13. Instant Demo Document Generation
    print("\n[Test 13] Instant Demo Document Generator Check (/api/documents/generate-demo/1)...")
    res_gen = client.post("/api/documents/generate-demo/1?doc_type=bank_passbook")
    assert res_gen.status_code == 200, f"Doc generation failed: {res_gen.text}"
    gen_doc = res_gen.json().get("document", {})
    assert gen_doc.get("doc_type") == "bank_passbook", "Unexpected doc_type"
    print(f" [PASS] Demo Document Generated: {gen_doc.get('doc_name')} (ID #{gen_doc.get('id')})")

    # 14. Chat Message Endpoint Alias (/api/chat/message)
    time.sleep(1.0)
    print("\n[Test 14] Chatbot Endpoint Alias Check (/api/chat/message)...")
    chat_alias_payload = {
        "session_id": "test_alias_session_202",
        "message": "What is the maximum loan under PM SVANidhi?",
        "user_id": 1
    }
    res_chat_alias = client.post("/api/chat/message", json=chat_alias_payload)
    assert res_chat_alias.status_code == 200, f"Chat alias failed: {res_chat_alias.text}"
    alias_json = res_chat_alias.json()
    assert alias_json.get("response") or alias_json.get("reply"), "Response missing"
    print(f" [PASS] Chatbot alias responded with response length: {len(alias_json.get('response') or '')}")

    # 15. LangGraph Full End-to-End Orchestration Workflow
    time.sleep(1.0)
    print("\n[Test 15] LangGraph StateGraph Full Pipeline Check (/api/workflow/run-full)...")
    run_full_payload = {
        "user_id": 1,
        "user_query": "I am a small farmer needing crop insurance or credit for organic farming.",
        "confirmed_criteria": ["Cultivable land under 2 hectares"]
    }
    res_full = client.post("/api/workflow/run-full", json=run_full_payload)
    assert res_full.status_code == 200, f"Full workflow failed: {res_full.text}"
    full_data = res_full.json()
    assert full_data.get("success") is True, "Workflow did not return success"
    assert len(full_data.get("recommendations", [])) >= 1, "Expected recommendations from LangGraph"
    print(f" [PASS] LangGraph 5-agent graph compiled and executed end-to-end!")
    print(f"        Recommended: {full_data['recommendations'][0]['name']}")

    print("\n" + "=" * 60)
    print(" [ALL 15 INTEGRATION TESTS PASSED SUCCESSFULLY!]")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
