# verify_fixes.py
import sys
sys.path.insert(0, '.')

from app.modules.risk.risk_engine import calculate_risk_score, get_risk_level
from app.modules.policy.policy_engine import determine_action

print("=" * 50)
print("RISK SCORING TESTS")
print("=" * 50)

tests = [
    # (findings, expected_score, expected_level)
    ([], 0, "low"),
    ([{"risk": "critical"}], 4, "medium"),
    ([{"risk": "critical"}, {"risk": "high"}], 7, "high"),
    ([{"risk": "critical"}, {"risk": "critical"}, {"risk": "critical"}], 12, "critical"),
    # Official spec sample: email(low) + password(critical) + api_key(high)
    ([{"risk": "low"}, {"risk": "critical"}, {"risk": "high"}], 8, "high"),
]

all_pass = True
for findings, exp_score, exp_level in tests:
    score = calculate_risk_score(findings)
    level = get_risk_level(score)
    status = "[OK] PASS" if score == exp_score and level == exp_level else "[FAIL] FAIL"
    if "[FAIL]" in status:
        all_pass = False
    print(f"{status} | score={score} (expected {exp_score}) | level={level} (expected {exp_level})")

print()
print("=" * 50)
print("POLICY ENGINE TESTS")
print("=" * 50)

policy_tests = [
    # (risk_level, options, expected_action)
    ("critical", {"block_high_risk": True, "mask": True},  "blocked"),
    ("high",     {"block_high_risk": True, "mask": True},  "blocked"),
    ("high",     {"block_high_risk": False, "mask": True},  "masked"),
    ("medium",   {"block_high_risk": False, "mask": True},  "masked"),
    ("low",      {"block_high_risk": True, "mask": True},   "allowed"),
    ("low",      {"block_high_risk": False, "mask": False},  "allowed"),
]

for risk_level, options, expected in policy_tests:
    action = determine_action(risk_level, options)
    status = "[OK] PASS" if action == expected else "[FAIL] FAIL"
    if "[FAIL]" in status:
        all_pass = False
    print(f"{status} | risk={risk_level} | options={options} -> action={action} (expected {expected})")

print()
print("=" * 50)
print("FINAL:", "[OK] ALL TESTS PASSED" if all_pass else "[FAIL] SOME TESTS FAILED")
print("=" * 50)
