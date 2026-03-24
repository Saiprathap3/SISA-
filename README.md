# AI Secure Data Intelligence Platform

## Problem Statement

Organizations need an automated way to detect sensitive data leaks, secrets, and suspicious behavior in text, logs, SQL, and files.

## Solution Architecture

Frontend → Backend → Claude/Anthropic API

```
[Browser] -> [Frontend React app] -> [FastAPI backend] -> [Anthropic API]
```

## Tech Stack

- Frontend: React + Vite
- Backend: FastAPI, Python
- AI: Anthropic (Claude) via SDK
- Tests: pytest

## Features

- Secret detection (API keys, tokens, passwords)
- Log analysis with brute-force and anomaly detection
- Risk scoring and policy enforcement
- Optional AI enrichment via Anthropic

## Quick Start

1. Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY`.
2. Build and run with Docker:

```bash
cp backend/.env.example backend/.env
docker-compose up --build
```

## API Usage

Health:

```bash
curl http://localhost:8000/health
```

Analyze:

```bash
curl -X POST http://localhost:8000/api/analyze -H 'Content-Type: application/json' -d '{"input_type":"log","content":"password=secret","options":{"mask_output":true,"use_ai":false,"block_on_critical":true}}'
```

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

## Evaluation Criteria Mapping

- Correct secret detection: regex engine
- Risk scoring: risk engine
- Policy enforcement: policy engine
# AI Secure Data Intelligence Platform

## Problem Statement
Protect sensitive data across logs, files, SQL, and chat by detecting, masking, and scoring risks, augmented by AI insights.

## Quick Start
1. Copy env: `cp backend/.env.example backend/.env` and fill `ANTHROPIC_API_KEY` and `API_BEARER_TOKEN`.
2. Build and run with Docker Compose:

```bash
docker-compose up --build
```

Backend: http://localhost:8000
Frontend: http://localhost:3000

## Features
- Multi-input analysis (text/file/sql/log/chat)
- Line-by-line log parser and detection
- Risk scoring and policy enforcement
- AI-powered insights via Claude (Anthropic SDK)

## Testing
Run backend tests:

```bash
cd backend
pytest tests/ -v --tb=short
```

## Architecture
- FastAPI backend
- React + Vite frontend
- Docker Compose for local deployment

