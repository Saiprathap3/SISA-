#!/usr/bin/env python3
"""Test the API endpoints"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("Waiting for server to be ready...")
time.sleep(3)

# Test 1: Health endpoint
print("\n" + "="*60)
print("TEST 1: Health Endpoint")
print("="*60)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print("✅ Health check passed")
        print(f"Model: {data.get('model')}")
        print(f"Version: {data.get('version')}")
        print(f"Status: {data.get('status')}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Patterns endpoint
print("\n" + "="*60)
print("TEST 2: Patterns Endpoint")
print("="*60)
try:
    response = requests.get(f"{BASE_URL}/patterns", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Patterns endpoint passed")
        print(f"Total patterns: {data.get('total')}")
        patterns = data.get('patterns', {})
        print(f"Pattern keys: {', '.join(list(patterns.keys())[:5])}...")
    else:
        print(f"❌ Patterns endpoint failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Analyze endpoint with text
print("\n" + "="*60)
print("TEST 3: Analyze Endpoint - Text Input")
print("="*60)
try:
    payload = {
        "input_type": "text",
        "content": "My email is admin@company.com and my password is hunter2. The API key is sk-prod-abc123def456ghi789jkl012",
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": True,
            "use_ai": True
        }
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print("✅ Analyze endpoint passed")
        print(f"Risk Level: {data.get('risk_level')}")
        print(f"Risk Score: {data.get('risk_score')}")
        print(f"Findings: {len(data.get('findings', []))} detected")
        print(f"Action: {data.get('action')}")
        print(f"Summary: {data.get('summary')}")
        print(f"AI Insights: {len(data.get('insights', []))} insights")
        print(f"Detection Breakdown: {json.dumps(data.get('detection_breakdown'), indent=2)}")
        
        # Show sample findings
        findings = data.get('findings', [])
        if findings:
            print("\nSample Findings:")
            for i, f in enumerate(findings[:3]):
                print(f"  {i+1}. Type: {f['type']}, Risk: {f['risk']}, Line: {f.get('line', 'N/A')}, Value: {f.get('value', 'N/A')[:30]}")
    else:
        print(f"❌ Analyze endpoint failed: {response.status_code}")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Analyze endpoint with log  
print("\n" + "="*60)
print("TEST 4: Analyze Endpoint - Log Input")
print("="*60)
try:
    log_content = """2026-03-25 10:00:01 INFO Login attempt user=admin@company.com
2026-03-25 10:00:02 ERROR Failed login for admin@company.com
2026-03-25 10:00:03 ERROR Failed login for admin@company.com
2026-03-25 10:00:04 ERROR Failed login for admin@company.com
2026-03-25 10:00:05 ERROR Failed login for admin@company.com
2026-03-25 10:00:06 ERROR Failed login for admin@company.com
2026-03-25 10:00:07 INFO Brute force attack detected from 192.168.1.10
2026-03-25 10:00:08 ERROR Debug mode enabled=true
2026-03-25 10:00:09 ERROR Stack trace: NullPointerException at service.java:45"""
    
    payload = {
        "input_type": "log",
        "content": log_content,
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": True,
            "use_ai": True
        }
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print("✅ Analyze endpoint (log) passed")
        print(f"Risk Level: {data.get('risk_level')}")
        print(f"Risk Score: {data.get('risk_score')}")
        print(f"Findings: {len(data.get('findings', []))} detected")
        print(f"Total Lines Analyzed: {data.get('total_lines_analyzed')}")
        
        # Show sample findings
        findings = data.get('findings', [])
        if findings:
            print("\nSample Findings:")
            for i, f in enumerate(findings[:3]):
                print(f"  {i+1}. Type: {f['type']}, Risk: {f['risk']}, Line: {f.get('line', 'N/A')}")
    else:
        print(f"❌ Analyze endpoint (log) failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Analyze endpoint with SQL
print("\n" + "="*60)
print("TEST 5: Analyze Endpoint - SQL Input")
print("="*60)
try:
    sql_content = "SELECT * FROM users WHERE 1=1; DROP TABLE users; UNION SELECT password FROM admin;"
    
    payload = {
        "input_type": "sql",
        "content": sql_content,
        "options": {
            "mask": True,
            "block_high_risk": True,
            "log_analysis": True,
            "use_ai": False
        }
    }
    response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print("✅ Analyze endpoint (SQL) passed")
        print(f"Risk Level: {data.get('risk_level')}")
        print(f"Risk Score: {data.get('risk_score')}")
        print(f"Findings: {len(data.get('findings', []))} detected")
        print(f"Action: {data.get('action')}")
    else:
        print(f"❌ Analyze endpoint (SQL) failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("✅ ALL TESTS COMPLETE")
print("="*60)
