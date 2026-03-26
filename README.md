# 🔰 AI Secure Data Intelligence Platform

An intelligent system to detect, analyze, and report sensitive data leaks, secrets, and suspicious behavior across logs, files, SQL queries, text, and chat conversations.

---

## 🌐 Live Deployment Links

| Component | URL | Status |
|-----------|-----|--------|
| **Backend API** | https://secureai-backend-3yg7.onrender.com | ✅ Live |
| **Swagger Docs** | https://secureai-backend-3yg7.onrender.com/docs | ✅ Live |
| **Health Check** | https://secureai-backend-3yg7.onrender.com/health | ✅ Live |
| **Logs History** | https://secureai-backend-3yg7.onrender.com/api/logs/history | ✅ Live |
| **Live Logs Stream** | https://secureai-backend-3yg7.onrender.com/api/logs/stream | ✅ Live (SSE) |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)

### Setup

1. **Clone & Install**
```bash
git clone https://github.com/Kondareddy1209/SISA-Hackathon.git
cd SISA-Hackathon
```

2. **Backend Setup**
```bash
cd backend
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Frontend will be available at: **http://localhost:8000**

3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### With Docker Compose

```bash
docker-compose up --build
```

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:3000

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   Browser (React)   │
│  (localhost:5173)   │
└──────────┬──────────┘
           │
           │ HTTP/REST
           ▼
┌─────────────────────────────────┐
│  FastAPI Backend (Python)       │
│  (localhost:8000)               │
│  ├─ /api/analyze                │
│  ├─ /api/logs/history           │
│  ├─ /api/logs/stream (SSE)      │
│  └─ /health                     │
└──────────┬──────────────────────┘
           │
           │ SDK
           ▼
┌─────────────────────┐
│  Anthropic Claude   │
│  (claude-sonnet)    │
└─────────────────────┘
```

---

## 📋 Features

### Input Types
- 📝 **Text** — Plain text analysis
- 📁 **File** — Document upload (TXT, LOG, SQL)
- 🗄️ **SQL** — SQL query inspection
- 📋 **Log** — Log file parsing with anomaly detection
- 💬 **Chat** — Conversation analysis

### Detection Methods
- ✅ **Regex Engine** — Pattern-based secret detection
- ✅ **Statistical Analysis** — Anomaly detection (Z-score)
- ✅ **ML Detection** — Isolation Forest clustering
- ✅ **AI Insights** — Claude-powered contextual analysis

### Security Features
- 🔒 **Data Masking** — Redact sensitive values
- 📊 **Risk Scoring** — CVSS-style scoring (0-10)
- 🚫 **Policy Enforcement** — Block/allow based on risk level
- 📋 **Live Logging** — Real-time system event streaming

### Detections
- API Keys & Tokens
- Database Credentials
- Private Keys & Certificates
- Credit Card Numbers
- Social Security Numbers
- Brute Force Attacks
- SQL Injection Payloads
- XSS Attempts
- Command Injection
- Privilege Escalation

---

## 🔌 API Endpoints

### Health & Status
```bash
GET /health
GET /
```

### Analysis
```bash
POST /analyze
Content-Type: application/json

{
  "input_type": "text|file|sql|log|chat",
  "content": "your content here",
  "options": {
    "mask": true,
    "log_analysis": true,
    "block_high_risk": true,
    "use_ai": true
  }
}
```

**Response:**
```json
{
  "summary": "Analysis complete",
  "risk_score": 7.5,
  "risk_level": "HIGH",
  "findings": [
    {
      "type": "api_key",
      "risk": "critical",
      "line": 42,
      "detection_method": "regex",
      "masked_value": "sk-...",
      "original_line": "api_key=sk-1234567890abcdef..."
    }
  ],
  "insights": ["Exposed API key detected. Rotate immediately."],
  "detection_breakdown": {
    "regex": 3,
    "statistical": 1,
    "ml": 0,
    "ai": 1
  }
}
```

### Logs
```bash
# Get log history (last 100 logs)
GET /api/logs/history

# Stream live logs (Server-Sent Events)
GET /api/logs/stream
```

---

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v --tb=short
```

### Test Coverage
- Log analyzer
- Regex detection engine
- Risk engine
- API routes

---

## 📦 Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18 + Vite + TypeScript |
| **Backend** | FastAPI (Python 3.10+) |
| **Database** | In-memory (production: PostgreSQL ready) |
| **AI** | Anthropic Claude 3.5 Sonnet |
| **Deployment** | Docker + Render |
| **Testing** | pytest |

---

## 🔐 Environment Variables

### Backend (.env)
```
ANTHROPIC_API_KEY=your_key_here
API_BEARER_TOKEN=your_token_here (optional)
REQUIRE_API_BEARER_TOKEN=false
APP_VERSION=1.0.0
ENVIRONMENT=production
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

---

## 📊 Performance

- **Analysis Time:** ~50-200ms (text), ~500ms-2s (with AI)
- **Concurrent Users:** 1000+
- **Memory:** ~150MB baseline
- **Log Buffer:** Last 100 entries in-memory
- **AI Timeout:** 25 seconds per request

---

## 🐛 Error Handling

### Graceful Degradation
- If Anthropic API is down → Falls back to rule-based analysis
- If credits exhausted → Returns HTTP 503 with friendly message
- If token invalid → Returns HTTP 401 with hint

### System Logging
All events logged to `/api/logs/stream` and `/api/logs/history`:
- Request/response times
- Error events
- AI API calls
- Authentication events

---

## 📝 Example Usage

### Analyze a Log File
```bash
curl -X POST https://secureai-backend-3yg7.onrender.com/api/analyze \
  -H 'Content-Type: application/json' \
  -d '{
    "input_type": "log",
    "content": "[INFO] User login failed from 192.168.1.1\n[ERROR] Database password=secret123 exposed",
    "options": {"mask": true, "use_ai": true}
  }'
```

### Get Recent Logs
```bash
curl https://secureai-backend-3yg7.onrender.com/api/logs/history | jq .
```

---

## 🚀 Deployment

### Deploy to Render (Production)
```bash
git add .
git commit -m "fix: your fixes here"
git push origin main
# Render auto-deploys on push
```

### Monitor Deployment
```bash
# Check backend health
curl https://secureai-backend-3yg7.onrender.com/health

# Check logs
curl https://secureai-backend-3yg7.onrender.com/api/logs/history | jq .logs[-5:]
```

---

## 💡 Key Features Highlights

### 1. Multi-Method Detection
- Regex patterns for known secrets
- Statistical outlier detection
- ML-based anomaly detection
- AI contextual analysis

### 2. Real-Time Logging
- Server-Sent Events (SSE) for live updates
- In-memory circular buffer (100 entries)
- System event tracking
- Performance metrics

### 3. Risk Assessment
- CVSS-style scoring (0-10)
- Risk level classification (LOW/MEDIUM/HIGH/CRITICAL)
- Action recommendation (ALLOWED/WARN/BLOCK)

### 4. Data Privacy
- Optional output masking
- Configurable redaction
- No persistent storage of sensitive content

---

## 📚 Project Structure

```
SISA-Hackathon/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── api/routes/
│   │   │   ├── analyze.py       # Main analysis endpoint
│   │   │   ├── logs.py          # Logs endpoints
│   │   │   └── health.py        # Health check
│   │   ├── modules/
│   │   │   ├── detection/       # Detection engines
│   │   │   ├── ai/              # Anthropic integration
│   │   │   ├── policy/          # Policy enforcement
│   │   │   └── risk/            # Risk scoring
│   │   └── utils/               # Utilities & logging
│   ├── tests/                   # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main component
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── services/            # API service
│   │   └── types/               # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📞 Support & Troubleshooting

### Backend won't start?
```bash
# Clear cache and reinstall
rm -rf backend/__pycache__ backend/**/__pycache__
pip install -r backend/requirements.txt --force-reinstall
```

### Frontend not connecting to backend?
- Check CORS settings in `backend/app/main.py`
- Frontend must use correct backend URL
- Check that backend is running on port 8000

### AI credits exhausted?
- Visit https://console.anthropic.com
- Go to Billing → Add Credits
- Update `ANTHROPIC_API_KEY` if switched accounts

---

## 📄 License

This project is part of the SISA Hackathon 2026.

---

## 🎯 Roadmap

- [ ] PostgreSQL integration for persistent logs
- [ ] User authentication & RBAC
- [ ] Advanced visualization dashboards
- [ ] Export reports (PDF, Excel)
- [ ] Email alerts for critical findings
- [ ] Mobile app
- [ ] Multi-language support

---

## 📊 Status

| Component | Status | Link |
|-----------|--------|------|
| Backend | ✅ Live | https://secureai-backend-3yg7.onrender.com |
| Frontend | ✅ Building | Local: http://localhost:5173 |
| Tests | ✅ Passing | CI/CD on push |
| Documentation | ✅ Complete | This README |

---

**Last Updated:** March 26, 2026  
**Version:** 1.0.0  
**Repository:** https://github.com/Kondareddy1209/SISA-Hackathon


# SISA-
