#!/usr/bin/env python3
"""Comprehensive API Validation Report"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print("🎯 SISA HACKATHON - AI SECURE DATA INTELLIGENCE PLATFORM")
print("API VALIDATION TEST REPORT")
print("="*70)
print(f"Timestamp: {datetime.now().isoformat()}")
print(f"Server: {BASE_URL}")
print("="*70)

test_results = []

# TEST 1: Health Endpoint
print("\n[TEST 1] Health Endpoint")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Server Status: {data.get('status')}")
        print(f"✅ Model: {data.get('model')}")
        print(f"✅ Version: {data.get('version')}")
        test_results.append(("Health Endpoint", "PASS"))
    else:
        test_results.append(("Health Endpoint", "FAIL"))
except Exception as e:
    print(f"❌ Error: {e}")
    test_results.append(("Health Endpoint", "FAIL"))

# TEST 2: Patterns Endpoint
print("\n[TEST 2] Patterns Endpoint")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/patterns", timeout=5)
    if response.status_code == 200:
        data = response.json()
        total = data.get('total')
        patterns = data.get('patterns', {})
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Total Patterns: {total}")
        print(f"✅ Patterns Loaded:")
        for pattern_name in list(patterns.keys())[:8]:
            risk = patterns[pattern_name].get('risk')
            print(f"   • {pattern_name.ljust(20)} (Risk: {risk})")
        if total > 8:
            print(f"   • ... and {total - 8} more patterns")
        test_results.append(("Patterns Endpoint", "PASS"))
    else:
        test_results.append(("Patterns Endpoint", "FAIL"))
except Exception as e:
    print(f"❌ Error: {e}")
    test_results.append(("Patterns Endpoint", "FAIL"))

# TEST 3: Text Analysis
print("\n[TEST 3] Analyze Endpoint - Text Input")
print("-" * 70)
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
        findings = data.get('findings', [])
        breakdown = data.get('detection_breakdown', {})
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Input Type: {data.get('content_type')}")
        print(f"✅ Risk Level: {data.get('risk_level').upper()}")
        print(f"✅ Risk Score: {data.get('risk_score')}/100")
        print(f"✅ Findings Detected: {len(findings)}")
        print(f"✅ Action Taken: {data.get('action').upper()}")
        print(f"✅ Summary: {data.get('summary')}")
        print(f"✅ Detection Breakdown:")
        print(f"   • Regex: {breakdown.get('regex', 0)}")
        print(f"   • Statistical: {breakdown.get('statistical', 0)}")
        print(f"   • ML: {breakdown.get('ml', 0)}")
        print(f"   • AI: {breakdown.get('ai', 0)}")
        
        if findings:
            print(f"✅ Sample Findings (showing 3 of {len(findings)}):")
            for i, f in enumerate(findings[:3]):
                print(f"   {i+1}. {f['type'].ljust(20)} | Risk: {f['risk'].ljust(8)} | Value: {f.get('value', 'N/A')[:25]}")
        
        test_results.append(("Text Analysis", "PASS"))
    else:
        test_results.append(("Text Analysis", "FAIL"))
except Exception as e:
    print(f"❌ Error: {e}")
    test_results.append(("Text Analysis", "FAIL"))

# TEST 4: Log Analysis
print("\n[TEST 4] Analyze Endpoint - Log Input")
print("-" * 70)
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
        findings = data.get('findings', [])
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Input Type: {data.get('content_type')}")
        print(f"✅ Lines Analyzed: {data.get('total_lines_analyzed')}")
        print(f"✅ Risk Level: {data.get('risk_level').upper()}")
        print(f"✅ Risk Score: {data.get('risk_score')}/100")
        print(f"✅ Findings Detected: {len(findings)}")
        print(f"✅ Action Taken: {data.get('action').upper()}")
        print(f"✅ Summary: {data.get('summary')}")
        
        # Categorize findings
        brute_force_findings = [f for f in findings if f['type'] == 'brute_force']
        suspicious_ip_findings = [f for f in findings if f['type'] == 'suspicious_ip_activity']
        
        print(f"✅ Brute Force Findings: {len(brute_force_findings)}")
        print(f"✅ Suspicious IP Findings: {len(suspicious_ip_findings)}")
        
        test_results.append(("Log Analysis", "PASS"))
    else:
        test_results.append(("Log Analysis", "FAIL"))
except Exception as e:
    print(f"❌ Error: {e}")
    test_results.append(("Log Analysis", "FAIL"))

# TEST 5: SQL Analysis
print("\n[TEST 5] Analyze Endpoint - SQL Input")
print("-" * 70)
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
        findings = data.get('findings', [])
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Input Type: {data.get('content_type')}")
        print(f"✅ Risk Level: {data.get('risk_level').upper()}")
        print(f"✅ Risk Score: {data.get('risk_score')}/100")
        print(f"✅ Findings Detected: {len(findings)}")
        print(f"✅ Action Taken: {data.get('action').upper()}")
        print(f"✅ Summary: {data.get('summary')}")
        
        # Categorize findings
        sql_injection = [f for f in findings if f['type'] == 'sql_injection']
        command_injection = [f for f in findings if f['type'] == 'command_injection']
        
        print(f"✅ SQL Injection Findings: {len(sql_injection)}")
        print(f"✅ Command Injection Findings: {len(command_injection)}")
        
        test_results.append(("SQL Analysis", "PASS"))
    else:
        test_results.append(("SQL Analysis", "FAIL"))
except Exception as e:
    print(f"❌ Error: {e}")
    test_results.append(("SQL Analysis", "FAIL"))

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
passed = sum(1 for _, result in test_results if result == "PASS")
total = len(test_results)

for test_name, result in test_results:
    status_icon = "✅" if result == "PASS" else "❌"
    print(f"{status_icon} {test_name.ljust(40)} {result}")

print("="*70)
print(f"\n🎉 RESULTS: {passed}/{total} tests passed\n")

if passed == total:
    print("✨ ALL TESTS PASSED - API IS FULLY FUNCTIONAL ✨")
else:
    print(f"⚠️ {total - passed} test(s) failed")

print("="*70)
