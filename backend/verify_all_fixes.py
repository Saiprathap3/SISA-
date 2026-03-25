#!/usr/bin/env python
import sys
import asyncio

sys.path.insert(0, '.')

from app.modules.detection.regex_engine import detect_all
from app.modules.risk.risk_engine import calculate_risk_score, get_risk_level
from app.modules.policy.policy_engine import determine_action
from app.modules.detection.log_analyzer import detect_brute_force

print("=" * 55)
print("VERIFICATION SUITE")
print("=" * 55)

# Test 1: Text with email + password + api_key
text = "email=admin@company.com password=hunter2 sk-prod-abc123def456ghi789"
findings = detect_all(text)
types_found = [f["type"] for f in findings]
t1 = all(t in types_found for t in ["email", "password", "api_key"])
print(f"{'PASS' if t1 else 'FAIL'} T1: Text detection — {types_found}")
if not t1:
    print(f"  Expected: email, password, api_key")
    print(f"  Got: {types_found}")

# Test 2: Secret detection
text2 = "secret=mysecretkey123"
f2 = detect_all(text2)
t2 = any(f["type"] in ["secret", "hardcoded_secret"] for f in f2)
print(f"{'PASS' if t2 else 'FAIL'} T2: Secret detection — {[f['type'] for f in f2]}")

# Test 3: Bearer token
text3 = "Bearer eyJhbGciOiJIUzI1NiJ9.test"
f3 = detect_all(text3)
t3 = any(f["type"] in ["bearer_token", "token"] for f in f3)
print(f"{'PASS' if t3 else 'FAIL'} T3: Bearer token — {[f['type'] for f in f3]}")

# Test 4: Risk scoring
findings_test = [{"risk": "critical"}, {"risk": "high"}, {"risk": "low"}]
score = calculate_risk_score(findings_test)
level = get_risk_level(score)
t4 = score == 8 and level == "high"
print(f"{'PASS' if t4 else 'FAIL'} T4: Risk scoring — score={score}, level={level}")
if not t4:
    print(f"  Expected: score=8, level=high")
    print(f"  Got: score={score}, level={level}")

# Test 5: Policy blocking
action = determine_action("critical", {"block_high_risk": True, "mask": True})
t5 = action == "blocked"
print(f"{'PASS' if t5 else 'FAIL'} T5: Policy block — action={action}")

# Test 6: Brute force
lines = ["FAILED login attempt for user admin"] * 6
bf = detect_brute_force(lines)
t6 = len(bf) > 0 and bf[0]["type"] == "brute_force"
print(f"{'PASS' if t6 else 'FAIL'} T6: Brute force — {bf[0]['type'] if bf else 'NOT DETECTED'}")

# Test 7: AI insights
async def test_ai():
    from app.modules.ai.claude_gateway import get_ai_insights
    findings = [{"type": "password", "risk": "critical", "line": 3}]
    insights = await get_ai_insights(findings, "log")
    t7 = len(insights) > 0 and isinstance(insights, list)
    print(f"{'PASS' if t7 else 'FAIL'} T7: AI insights — {len(insights)} insights, First: {insights[0][:60] if insights else 'EMPTY'}")
    return t7

t7 = asyncio.run(test_ai())

print("=" * 55)
all_pass = all([t1, t2, t3, t4, t5, t6, t7])
print(f"RESULT: {'✅ ALL TESTS PASSED' if all_pass else '❌ SOME TESTS FAILED'}")
print("=" * 55)
