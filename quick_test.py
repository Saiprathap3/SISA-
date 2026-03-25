#!/usr/bin/env python3
"""Quick API test without AI"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("Waiting for server to be ready...")
time.sleep(2)

# Test 1: Health endpoint
print("\n✅ Health Endpoint Test")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"  Status: {data.get('status')}")
        print(f"  Model: {data.get('model')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Patterns endpoint
print("\n✅ Patterns Endpoint Test")
try:
    response = requests.get(f"{BASE_URL}/patterns", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"  Total patterns: {data.get('total')}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Analyze endpoint with text (NO AI)
print("\n✅ Analyze Endpoint - Text Input (NO AI)")
try:
    payload = {
        "input_type": "text",
        "content": "My email is admin@company.com and my password is hunter2. The API key is sk-prod-abc123def456ghi789jkl012",
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": True,
            "use_ai": False
        }
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  Risk Level: {data.get('risk_level')}")
        print(f"  Risk Score: {data.get('risk_score')}")
        print(f"  Findings: {len(data.get('findings', []))} detected")
        print(f"  Action: {data.get('action')}")
        print(f"  Detection Breakdown: {data.get('detection_breakdown')}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Analyze endpoint with log (NO AI)
print("\n✅ Analyze Endpoint - Log Input (NO AI)")
try:
    log_content = """2026-03-25 10:00:01 INFO Login attempt user=admin@company.com
2026-03-25 10:00:02 ERROR Failed login for admin@company.com
2026-03-25 10:00:03 ERROR Failed login for admin@company.com
2026-03-25 10:00:04 ERROR Failed login for admin@company.com
2026-03-25 10:00:05 ERROR Failed login for admin@company.com
2026-03-25 10:00:06 ERROR Failed login for admin@company.com
2026-03-25 10:00:07 INFO Suspicious IP 192.168.1.10
2026-03-25 10:00:08 ERROR Debug mode enabled=true
2026-03-25 10:00:09 ERROR Stack trace: NullPointerException at service.java:45"""
    
    payload = {
        "input_type": "log",
        "content": log_content,
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": True,
            "use_ai": False
        }
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  Risk Level: {data.get('risk_level')}")
        print(f"  Risk Score: {data.get('risk_score')}")
        print(f"  Findings: {len(data.get('findings', []))} detected")
        print(f"  Total Lines: {data.get('total_lines_analyzed')}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Analyze endpoint with SQL (NO AI)
print("\n✅ Analyze Endpoint - SQL Input (NO AI)")
try:
    sql_content = "SELECT * FROM users WHERE 1=1; DROP TABLE users; UNION SELECT password FROM admin;"
    
    payload = {
        "input_type": "sql",
        "content": sql_content,
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": False,
            "use_ai": False
        }
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  Risk Level: {data.get('risk_level')}")
        print(f"  Risk Score: {data.get('risk_score')}")
        print(f"  Findings: {len(data.get('findings', []))} detected")
        print(f"  Action: {data.get('action')}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("✅ ALL QUICK TESTS COMPLETE")
print("="*60)
