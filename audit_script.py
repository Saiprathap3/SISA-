import sys
import json
import os
from fastapi.testclient import TestClient

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

# Set environment variables for testing
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-api03-test-key"
os.environ["PYTHONUTF8"] = "1"

from app.main import app

client = TestClient(app)

def run_audit():
    results = {}

    print("\n--- BLOCK A: BACKEND DESIGN ---")
    try:
        r = client.post("/api/analyze", json={
            "input_type": "text", 
            "content": "test", 
            "options": {"mask": True, "log_analysis": False, "block_high_risk": False}
        })
        results["A1"] = "PASS" if r.status_code == 200 else f"FAIL ({r.status_code})"
        print(f"A1 API Existence: {results['A1']}")
        if r.status_code == 200:
            body = r.json()
            required_keys = ["summary", "findings", "risk_score", "risk_level", "action", "insights"]
            missing = [k for k in required_keys if k not in body]
            results["A3"] = "PASS" if not missing else f"FAIL (Missing {missing})"
            print(f"A3 Schema Compliance: {results['A3']}")
    except Exception as e:
        results["A1"] = f"FAIL (Error: {e})"
        print(f"A1: {results['A1']}")

    # TEST A2: Schema Validation (Sending spec fields)
    payload_spec = {
        "input_type": "log",
        "content": "test log content",
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": True
        }
    }
    r_a2 = client.post("/api/analyze", json=payload_spec)
    results["A2"] = "PASS" if r_a2.status_code == 200 else f"FAIL ({r_a2.status_code})"
    print(f"A2 Request Validation: {results['A2']}")

    print("\n--- BLOCK B: LOG ANALYSIS ---")
    sample_log = """2026-03-10 10:00:01 INFO User login
email=admin@company.com
password=admin123
api_key=sk-prod-xyz
ERROR stack trace: NullPointerException
at service.java:45"""
    r_b1 = client.post("/api/analyze", json={
        "input_type": "log",
        "content": sample_log,
        "options": {"mask": True, "log_analysis": False, "block_high_risk": True}
    })
    if r_b1.status_code == 200:
        data = r_b1.json()
        findings = data.get("findings", [])
        types = [f["type"] for f in findings]
        results["B1_findings"] = "PASS" if all(t in types for t in ["email", "password", "api_key"]) else f"FAIL (Found {types})"
        # Spec sample: email(low=1) + password(critical=4) + api_key(critical=4) = 9
        # Wait, in spec B2, api_key is HIGH(3). So 1+4+3 = 8.
        results["B1_score"] = "PASS" if data.get("risk_score") == 8 else f"FAIL (Score {data.get('risk_score')})"
        results["B4_line"] = "PASS" if all("line" in f for f in findings) else "FAIL"
    else:
        results["B1"] = f"FAIL ({r_b1.status_code})"
    
    print(f"B1 Findings: {results.get('B1_findings', 'N/A')}")
    print(f"B1 Score: {results.get('B1_score', 'N/A')}")
    print(f"B4 Line Tracking: {results.get('B4_line', 'N/A')}")

    print("\n--- BLOCK D: RISK ENGINE ---")
    # 1 password (critical=4) + 1 api_key (critical in regex_engine=4)
    # Wait, regex_engine.py says api_key is 'critical'. Spec says 'high'.
    # For now, let's use the actual values in the code.
    r_d1 = client.post("/api/analyze", json={
        "input_type": "log",
        "content": "password=test\napi_key=sk-123",
        "options": {"mask": False, "log_analysis": False, "block_high_risk": False}
    })
    if r_d1.status_code == 200:
        data = r_d1.json()
        # Code: password(4) + api_key(3) = 7
        results["D1"] = "PASS" if data.get("risk_score") == 7 else f"FAIL (Score {data.get('risk_score')})"
        results["D2"] = "PASS" if data.get("risk_level") == "high" else f"FAIL (Level {data.get('risk_level')})"
    print(f"D1 Scoring Math: {results.get('D1', 'N/A')}")
    print(f"D2 Level Threshold: {results.get('D2', 'N/A')}")

    print("\n--- BLOCK E: POLICY ENGINE ---")
    r_e1 = client.post("/api/analyze", json={
        "input_type": "log",
        "content": "password=test",
        "options": {"mask": True, "log_analysis": False, "block_high_risk": True}
    })
    if r_e1.status_code == 200:
        # Score 4 -> Medium -> should NOT be blocked by the user's logic unless "medium" is blocked?
        # User fix 2 says: "if risk_level == 'critical' and block_high_risk -> blocked"
        # "if risk_level == 'high' and block_high_risk -> blocked"
        # Score 4 is "medium". So it should be "masked".
        results["E1"] = "PASS" if r_e1.json().get("action") == "masked" else f"FAIL (Action {r_e1.json().get('action')})"
    print(f"E1 Policy Policy Action: {results.get('E1', 'N/A')}")

    # Output full report summary
    with open("audit_results_final.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_audit()
