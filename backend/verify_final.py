import sys

sys.path.insert(0, ".")

from app.modules.detection.regex_engine import detect_all
from app.modules.risk.risk_engine import calculate_risk_score, get_risk_level
from app.modules.policy.policy_engine import determine_action

print("=" * 55)
print("FINAL VERIFICATION")
print("=" * 55)

# FIX 1: Policy — HIGH should be BLOCKED
action1 = determine_action("high", {"block_high_risk": True, "mask": True})
t1 = action1 == "blocked"
print(f"{'PASS' if t1 else 'FAIL'} FIX1a: HIGH+block_critical → {action1}")

action2 = determine_action("critical", {"block_high_risk": True})
t2 = action2 == "blocked"
print(f"{'PASS' if t2 else 'FAIL'} FIX1b: CRITICAL+block_critical → {action2}")

action3 = determine_action("medium", {"block_high_risk": True, "mask": True})
t3 = action3 == "masked"
print(f"{'PASS' if t3 else 'FAIL'} FIX1c: MEDIUM+mask → {action3}")

action4 = determine_action("low", {"block_high_risk": True, "mask": True})
t4 = action4 == "allowed"
print(f"{'PASS' if t4 else 'FAIL'} FIX1d: LOW → {action4}")

# FIX 2: Risk scoring
f_xss = [{"risk": "high"}, {"risk": "high"}]  # xss + command_inj
score2 = calculate_risk_score(f_xss)
level2 = get_risk_level(score2)
t5 = score2 == 6 and level2 == "medium"
print(f"{'PASS' if t5 else 'FAIL'} FIX2a: 2x HIGH = score={score2} level={level2}")

f_ssn = [{"risk": "critical"}, {"risk": "critical"}]
score3 = calculate_risk_score(f_ssn)
level3 = get_risk_level(score3)
t6 = score3 == 8 and level3 == "high"
print(f"{'PASS' if t6 else 'FAIL'} FIX2b: SSN+CC = score={score3} level={level3}")

# FIX 3: Email detection
text = "My email is admin@company.com and my password is hunter2. The API key is sk-prod-abc123def456ghi789jkl012"
findings = detect_all(text)
types = [f["type"] for f in findings]
t7 = "email" in types
t8 = "password" in types
t9 = "api_key" in types
print(f"{'PASS' if t7 else 'FAIL'} FIX3a: email detected — {types}")
print(f"{'PASS' if t8 else 'FAIL'} FIX3b: password detected")
print(f"{'PASS' if t9 else 'FAIL'} FIX3c: api_key detected")

# Official spec §9 test
spec_log = """2026-03-10 10:00:01 INFO User login
email=admin@company.com
password=admin123
api_key=sk-prod-xyz
ERROR stack trace: NullPointerException at service.java:45"""
f_spec = detect_all(spec_log)
t_spec_types = [f["type"] for f in f_spec]
risks = [f["risk"] for f in f_spec]
score_spec = calculate_risk_score(f_spec)
level_spec = get_risk_level(score_spec)
action_spec = determine_action(level_spec, {"block_high_risk": True, "mask": True})
t10 = "email" in t_spec_types
t11 = "password" in t_spec_types
t12 = "api_key" in t_spec_types
t13 = action_spec == "blocked"
print(f"{'PASS' if t10 else 'FAIL'} SPEC: email found")
print(f"{'PASS' if t11 else 'FAIL'} SPEC: password found")
print(f"{'PASS' if t12 else 'FAIL'} SPEC: api_key found")
print(f"{'PASS' if t13 else 'FAIL'} SPEC: action={action_spec} (expected blocked)")
print(f"       score={score_spec}, level={level_spec}")

print("=" * 55)
all_ok = all([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13])
print(f"RESULT: {'ALL FIXED' if all_ok else 'STILL HAS ISSUES'}")
print("=" * 55)
