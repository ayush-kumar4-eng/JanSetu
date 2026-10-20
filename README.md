# JanSetu (जनसेतु) — Agentic AI Workforce for Government Scheme Navigation

> **AI-Driven Citizen Empowerment for Last-Mile Welfare Discovery and Delivery**  
> *Built for Hackathons & Prototype Demonstrations*

---

## ⚠️ Important Safety & Demonstration Disclaimer

**JanSetu is an AI demonstration prototype created strictly for hackathons and academic evaluation.**  
- **Not an Official Government Portal:** This application is not affiliated with or endorsed by any Government ministry or department.
- **Simulated Submissions:** No actual applications are submitted to government agencies. All submission IDs (e.g., `JS-2025-XXXXX`), status transitions, and timeline tracking are simulated.
- **No Sensitive Identity Transmissions:** Real Aadhaar numbers, PAN numbers, or sensitive documents should never be uploaded. The platform utilizes dummy demo documents and sample persona data.
- **Human-in-the-Loop:** Explicit user approval is mandatory before any application draft is finalized.

---

## 🌟 Project Overview

Over 700+ central and state government schemes exist in India, yet millions of eligible citizens miss out due to:
1. **Language & Complex Jargon:** Scheme guidelines are written in bureaucratic language.
2. **Scattered Information:** Citizens do not know which department or ministry manages which scheme.
3. **Document Uncertainty:** Citizens get rejected simply for missing one non-critical certificate.
4. **Application Friction:** Filling multi-page official forms is intimidating.

**JanSetu** solves this with an **Agentic AI Workforce** powered by **LangGraph**, **Groq (Llama 3.3)**, **Gemini Fallback**, and **Qdrant Vector Search**. Citizens simply describe their life situation in conversational plain language (e.g. *"I am a street vendor in Jaipur earning ₹1.2 lakh looking for a small loan for my cart"*). 

JanSetu's multi-agent collective takes over:
- 🎯 **Intake Agent:** Understands citizen situation & extracts structured criteria.
- 🔍 **Scheme Matcher Agent:** Performs semantic search across welfare database & presents top 2–3 recommendations with clear rationale.
- ⚖️ **Eligibility Assessor Agent:** Audits criteria (age, income, occupation, landholding) and highlights fulfilled vs self-declarable requirements.
- 📑 **Document Readiness Agent:** Cross-references required documents with uploaded demo files, flagging ready vs missing documents.
- ✍️ **Application Drafter Agent:** Compiles official application draft with justification statement for explicit human review.
- 🚀 **Simulated Submission Engine:** Issues tracking reference, timeline milestone alerts, and status events.
- 💬 **JanSetu Mitra (Chatbot):** Sidebar scheme advisor for interactive Q&A anytime.

---

## 🏗️ Architecture & Technology Stack

```
   ┌──────────────────────────────────────────────────────────────┐
   │                   Frontend (HTML/CSS/JS)                     │
   │  Modern Glassmorphism UI • 5-Step Stepper • JanSetu Mitra    │
   └──────────────────────────────▲───────────────────────────────┘
                                  │ REST API / JSON
   ┌──────────────────────────────▼───────────────────────────────┐
   │                     Backend (FastAPI)                        │
   │                                                              │
   │  ┌────────────────────────────────────────────────────────┐  │
   │  │             LangGraph Multi-Agent Workflow             │  │
   │  │  1. Intake  -> 2. Matcher -> 3. Assessor              │  │
   │  │  4. Document Readiness   -> 5. Application Drafter     │  │
   │  └────────────────────────────────────────────────────────┘  │
   │                                                              │
   │  ┌────────────────────┐  ┌─────────────────────────────────┐ │
   │  │  LLM Engine        │  │  Semantic Vector Search         │ │
   │  │  • Groq (Primary)  │  │  • Qdrant (Local / Cloud)       │ │
   │  │  • Gemini Fallback │  │  • Multilingual Embeddings      │ │
   │  └────────────────────┘  └─────────────────────────────────┘ │
   └──────────────────────────────▲───────────────────────────────┘
                                  │
   ┌──────────────────────────────▼───────────────────────────────┐
   │                   Database (SQLite)                          │
   │  Users • Citizen Profiles • Schemes Catalog • Documents     │
   │  Applications • Tracking Timeline • Notifications • Chat     │
   └──────────────────────────────────────────────────────────────┘
```

### Tech Stack Details:
- **Frontend:** Vanilla HTML5, Modern CSS3 (Glassmorphism, custom design system, mobile responsive), Vanilla ES6+ JavaScript.
- **Backend:** Python 3.10+ / 3.13, FastAPI, Uvicorn, Pydantic, python-dotenv.
- **Agent Orchestration:** LangGraph & LangChain.
- **Primary LLM:** Groq (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`).
- **Fallback LLM:** Google Gemini (`gemini-2.0-flash` / `gemini-1.5-flash`).
- **Vector Search:** Qdrant (`qdrant-client` with local disk persistence or Qdrant Cloud).
- **Relational DB:** SQLite with schema for users, profiles, schemes, applications, and logs.

---

## 📁 Simple Folder Structure

```
JanSetu/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── workflow.py       # 5 LangGraph workflow agents
│   │   └── chatbot.py        # JanSetu Mitra sidebar assistant
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # User & Citizen Profile management
│   │   ├── schemes.py        # Scheme directory & search
│   │   ├── workflow.py       # Workflow progression API endpoints
│   │   ├── documents.py      # Demo doc upload & verification
│   │   ├── applications.py   # Application tracking & timeline
│   │   └── chat.py           # Chatbot messaging
│   ├── config.py             # Environment configuration
│   ├── db.py                 # SQLite database connection & CRUD
│   ├── llm_client.py         # Groq + Gemini LLM fallback client
│   ├── vector_search.py      # Qdrant semantic search engine
│   ├── main.py               # FastAPI entrypoint & static mounting
│   ├── requirements.txt      # Backend Python dependencies
│   ├── .env.example          # Environment template
│   └── .env                  # Environment secrets (user-provided)
├── database/
│   ├── schema.sql            # Relational database schema
│   ├── schemes_seed.json     # Comprehensive Indian government schemes
│   ├── init_db.py            # SQLite & Qdrant initialization script
│   └── jansetu.db            # Auto-generated SQLite database
├── frontend/
│   ├── index.html            # Main Single-Page Application
│   ├── style.css             # Glassmorphism design system & animations
│   └── app.js                # Frontend controllers & state engine
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start Guide (Windows Terminal)

### 1. Clone or Open Workspace
Open PowerShell in the `JanSetu` directory:
```powershell
cd c:\Users\ayush\OneDrive\Desktop\JanSetu
```

### 2. Set Up Python Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables
Copy `backend/.env.example` to `backend/.env` and edit your API keys:
```powershell
cp backend/.env.example backend/.env
```
Open `backend/.env` and add:
- `GROQ_API_KEY=your_groq_api_key_here`
- *(Optional)* `GEMINI_API_KEY=your_gemini_api_key_here`
- *(Optional)* `QDRANT_URL=` (leave blank for zero-setup local embedded Qdrant storage)

> *Note: Even if keys are empty during initial setup, JanSetu includes an intelligent local fallback inference engine so you can explore the demo immediately!*

### 5. Initialize Database & Scheme Vector Index
Run the ingestion script to create tables, seed 14+ government schemes, and build the Qdrant semantic index:
```powershell
python database/init_db.py
```

### 6. Start the Application Server
```powershell
python backend/main.py
```
Open your browser at:
👉 **`http://localhost:8000`**

---

## 🧪 12-Step Complete User Journey Walkthrough

1. **User Profile:** Switch between preset personas (*Ramesh Kumar - Farmer*, *Sunita Devi - Street Vendor*, *Pooja Sharma - Student*) or customize your citizen details.
2. **Plain Language Intake:** Describe what you need (e.g. *"I need a loan to buy goods for my roadside cart"*).
3. **AI Recommendation:** The AI analyzes your query against Qdrant and highlights the top 2–3 matching schemes (e.g. **PM SVANidhi** with a 94% match score).
4. **Scheme Selection:** Pick your preferred scheme.
5. **Eligibility Audit:** The AI verifies your age, occupation, and income against the scheme criteria.
6. **Checklist Confirmation:** Review criteria and confirm any self-declaration items.
7. **Document Readiness:** View ready vs missing documents (Aadhaar, Vending Certificate, Bank Passbook).
8. **Demo Document Upload:** Click "Generate Demo Document" or upload sample mock files.
9. **AI Application Drafter:** The Drafter Agent generates a completed official form draft with a formal justification statement.
10. **Explicit Review & Approval:** Review the draft and check the explicit agreement box.
11. **Simulated Submission:** Click Submit to send in demo mode.
12. **Live Tracking:** Receive a generated Reference Number (e.g. `JS-2025-78412`), view the 4-stage tracking timeline (*Submitted* → *Officer Review* → *Field Check* → *Sanctioned*), and view simulated notifications.
13. **JanSetu Mitra Chatbot:** Ask questions anytime via the floating sidebar widget.

---

## 🔒 Security & Privacy Practices
- All API keys reside exclusively in `backend/.env`.
- Frontend never has access to secret tokens.
- No real PII or Aadhaar biometric data is handled or stored.
- Explicit human consent required before draft completion.
