# 🔰 AI Secure Data Intelligence Platform (SOC Dashboard)

An enterprise-grade, intelligent Security Operations Center (SOC) system designed to detect, analyze, and report sensitive data leaks, secrets, and suspicious behaviors in real-time across logs, files, SQL queries, text, and chat conversations. 

Equipped with a modern, glassmorphism-powered Cyber UI.

---

## ✨ Key Features Highlights

### 🎨 Premium Cyber-Themed UI
- Professional SOC Aesthetic: Deep cyber dark (`#0B0F1A`) background with subtle animated grid radial gradients.
- Glassmorphism Panels: UI elements utilize frosted-glass blurring effects paired with neon cyan (`#00FFC6`) accents.
- Micro-Interactions: Smooth 0.3s cubic bézier transitions, hover glow states, slide-up animations, and dynamically pulsing risk severity badges.
- Security Dashboard Layout: A perfectly proportioned split-view interface tracking "System Status" and "Risk Scores" in real time.

### 🧠 Multi-Layer Detection Engine
- Regex Patterns: Lightning-fast pattern matching for known secrets (API Keys, JWTs, Passwords, etc.).
- Statistical Analysis: Outlier detection using Z-scoring models to catch unusual frequencies (e.g., automated brute force limits).
- Machine Learning (ML): Isolation Forest clustering to detect anomalous patterns outside of normal operation.
- AI Contextual Insights: Powered by Anthropic's Claude 3.5 Sonnet to infer context, provide plain-english forensic insights, and generate security recommendations.

### 🛡️ Core Security Capabilities
- Automated Data Masking: Redacts sensitive payloads automatically before displaying them on the screen.
- CVSS-Style Risk Scoring (0-10): Every scan is scored and categorized into `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.
- Policy Enforcement: Built-in rules engine that determines whether to `ALLOW`, `WARN`, or `BLOCK` the operation based on the evaluated risk level.
- Live SOC Logs: Real-time Server-Sent Events (SSE) tracking system events directly in the dashboard's Live Viewer.

### 📁 Varied Input Parsing
- 📝 Text — Direct plain text validation.
- 📁 File Drop — Parses uploaded documents and text files (.txt, .log, .sql).
- 🗄️ SQL — Specialized parsing for SQL injections and schema exposure.
- 📋 Raw Logs — Dedicated multi-line log chunk parsing.
- 💬 Chat — Conversation context tracker.

---

## 📂 Complete Source Code Structure

```text
SISA Hackathon/
├── backend/                      # FastAPI Python Backend
│   ├── app/                      # Core application logic
│   │   ├── api/                  # REST API routers
│   │   ├── core/                 # Configs and Security Policies
│   │   ├── engine/               # Detection Engine (Regex, ML, NLP)
│   │   ├── models/               # Pydantic Schemas
│   │   └── services/             # AI Integration (Anthropic Claude 3.5 Sonnet)
│   ├── tests/                    # Backend test suites (PyTest)
│   ├── requirements.txt          # Backend dependencies
│   ├── Dockerfile                # Backend Docker configuration
│   ├── start.bat                 # Helper script for running backend Server
│   └── .env.example              # Example environment variables
│
├── frontend/                     # React + Vite Frontend
│   ├── src/                      # Source Code
│   │   ├── components/           # React Components (Glassmorphism Cyber UI)
│   │   ├── App.tsx               # Main Dashboard layout and routing
│   │   ├── main.tsx              # React entry point
│   │   └── styles.css            # Global UI styling and Cyber Effects
│   ├── package.json              # NPM dependencies
│   └── Dockerfile                # Frontend Docker configuration
│
├── docker-compose.yml            # Multi-container Docker orchestration script
└── README.md                     # Platform Documentation (You are here!)
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Backend Setup (FastAPI)
The backend employs a Python web server, but we've included an NPM wrapper for developer convenience!

```bash
cd backend

# Create your virtual environment and install dependencies
python -m venv .venv_new
.venv_new\Scripts\activate   # On Windows
source .venv_new/bin/activate # On Mac/Linux
pip install -r requirements.txt

# Or simply use the bridged NPM command to run the backend server!
npm start
```
(Backend will spin up on `http://localhost:8000`)

### 2. Frontend Setup (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
(Frontend will compile and open on `http://localhost:5173`)

---

## 🔌 API Endpoints Reference

### Analysis
```http
POST /analyze
Content-Type: application/json

{
  "input_type": "text|file|sql|log|chat",
  "content": "your target payload or logs here",
  "options": {
    "mask": true,
    "log_analysis": true,
    "block_high_risk": true,
    "use_ai": true
  }
}
```

### Logs & Health
```http
GET /health                  # View system status, current model, and uptime
GET /api/logs/history        # Fetch last 100 system events (Buffer)
GET /api/logs/stream         # Connect to the live Server-Sent Events (SSE) stream
```

---

## 🔒 Environment Variables Configuration

### Backend Requirements
Make sure to map your backend variables properly by duplicating `backend/.env.example` to `backend/.env`:

```env
ANTHROPIC_API_KEY=your_key_here
API_BEARER_TOKEN=sisa-hackathon-secure-2025
REQUIRE_API_BEARER_TOKEN=false
FRONTEND_ORIGIN=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

### Frontend Requirements
For the frontend, the default configuration points to `http://localhost:8000`. If you need to change this, create/edit the `.env.development` (or `.env.production`) file inside the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend UI | React 18, Vite, TypeScript, Custom CSS Glassmorphism |
| Backend API | FastAPI, Uvicorn (Python 3.12) |
| Threat AI | Anthropic Claude 3.5 Sonnet API |
| Testing | PyTest |
| Deployment | Docker / Render.com |

---

## 🧪 Running Tests

To execute the backend testing suites to verify bug patching and policy routing:

```bash
cd backend
.venv_new\Scripts\activate
python verify_final.py
```

---

## 📄 License
This platform is part of the SISA Hackathon 2026.
