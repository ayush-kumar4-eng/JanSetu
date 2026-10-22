"""
JanSetu Mitra — Scheme Search and Advisory Chatbot
Reuses Qdrant semantic search and conversational history to answer citizen questions.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from backend.db import get_chat_history, save_chat_message, get_user_by_id
from backend.llm_client import invoke_llm
from backend.vector_search import search_schemes

logger = logging.getLogger("JanSetu.Chatbot")


def handle_chat_message(session_id: str, message: str, user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Processes user query using Qdrant semantic retrieval and conversational LLM response.
    """
    logger.info(f"Chat message received for session '{session_id}': {message[:60]}...")

    # 1. Fetch user context if user_id is provided
    user_context = ""
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            user_context = (
                f"\n[Active Citizen Profile Context]\n"
                f"- Name: {user.get('full_name')}\n"
                f"- Occupation: {user.get('occupation')}, Age: {user.get('age')}\n"
                f"- Annual Income: Rs {user.get('annual_income')}\n"
                f"- Location: {user.get('district')}, {user.get('state')} ({user.get('residence_area')})\n"
                f"- Landholding: {user.get('land_ownership_hectares')} hectares\n"
            )

    # 2. Retrieve scheme knowledge using Qdrant vector search
    retrieved_schemes = search_schemes(message, limit=3)
    scheme_context_texts = []
    for s in retrieved_schemes:
        scheme_context_texts.append(
            f"Scheme: {s['name']} ({s.get('code')})\n"
            f"Ministry: {s['ministry']}\n"
            f"Category: {s['category']}\n"
            f"Benefits: {s['benefits']}\n"
            f"Eligibility: {s.get('eligibility_criteria', {}).get('key_rules', [])}\n"
            f"Required Documents: {s.get('required_documents', [])}\n"
            f"Official Link: {s.get('official_url', '')}"
        )

    knowledge_context = "\n---\n".join(scheme_context_texts)

    # 3. Fetch past conversation turns
    recent_history = get_chat_history(session_id, limit=6)
    history_str = ""
    for h in recent_history:
        role = "Citizen" if h["sender"] == "user" else "JanSetu Mitra"
        history_str += f"{role}: {h['message']}\n"

    # 4. Prompt Assembly
    system_prompt = f"""
You are "JanSetu Mitra" (जनसेतु मित्र), an empathetic, deeply knowledgeable AI Welfare Advisor.
Your mission is to guide Indian citizens through government welfare schemes, explain eligibility criteria,
detail necessary documents, and assist with application navigation.

Tone Guidelines:
- Respectful, encouraging, culturally aware, and crystal clear.
- Avoid bureaucratic legalese; explain terms in simple, practical language.
- Mention specific scheme names, monetary amounts, and official portals when applicable.
- If relevant documents are needed, enumerate them clearly with bullet points.
- Always include a reassuring reminder that JanSetu can guide them to prepare a demo application.
- Format responses cleanly with bolding and bullet points.

{user_context}

[Official Knowledge Base (Semantic Search Matches)]:
{knowledge_context}
"""

    user_prompt = f"""
[Conversation History]:
{history_str}

Citizen's Current Message:
{message}
"""

    # 5. Invoke LLM
    assistant_reply = invoke_llm(user_prompt, system_prompt)

    # 6. Save message history in DB
    save_chat_message(session_id, "user", message, user_id=user_id)
    save_chat_message(
        session_id,
        "assistant",
        assistant_reply,
        user_id=user_id,
        metadata={"cited_schemes": [s["code"] for s in retrieved_schemes]}
    )

    # 7. Formulate dynamic suggested follow-up questions
    if retrieved_schemes:
        top_s = retrieved_schemes[0]
        code_or_name = top_s.get("code") or (top_s["name"][:25] + "...")
        suggested_prompts = [
            f"What documents do I need for {code_or_name}?",
            f"Am I eligible for {code_or_name}?",
            "How do I apply on the official portal?"
        ]
    else:
        suggested_prompts = [
            "What scholarships are available for college students?",
            "How does Ayushman Bharat health insurance work?",
            "How can street vendors get loans under PM SVANidhi?"
        ]

    return {
        "reply": assistant_reply,
        "cited_schemes": retrieved_schemes,
        "suggested_prompts": suggested_prompts,
        "session_id": session_id
    }
