#!/usr/bin/env python3
"""Quick verification of all backend modules"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Testing imports...")

try:
    from app.core.config import settings
    print("✅ config.py imports OK")
except Exception as e:
    print(f"❌ config.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.detection.regex_engine import detect_all, get_all_patterns
    print("✅ regex_engine.py imports OK")
except Exception as e:
    print(f"❌ regex_engine.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.detection.log_analyzer import analyze_log
    print("✅ log_analyzer.py imports OK")
except Exception as e:
    print(f"❌ log_analyzer.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.detection.statistical_detector import detect_statistical_anomalies
    print("✅ statistical_detector.py imports OK")
except Exception as e:
    print(f"❌ statistical_detector.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.detection.ml_detector import detect_ml_anomalies
    print("✅ ml_detector.py imports OK")
except Exception as e:
    print(f"❌ ml_detector.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.risk.risk_engine import calculate_risk_score, get_risk_level, get_risk_summary
    print("✅ risk_engine.py imports OK")
except Exception as e:
    print(f"❌ risk_engine.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.policy.policy_engine import determine_action, apply_masking
    print("✅ policy_engine.py imports OK")
except Exception as e:
    print(f"❌ policy_engine.py import failed: {e}")
    sys.exit(1)

try:
    from app.modules.ai.claude_gateway import get_ai_insights
    print("✅ claude_gateway.py imports OK")
except Exception as e:
    print(f"❌ claude_gateway.py import failed: {e}")
    sys.exit(1)

try:
    from app.api.routes.analyze import router
    print("✅ analyze.py route imports OK")
except Exception as e:
    print(f"❌ analyze.py route import failed: {e}")
    sys.exit(1)

try:
    from app.main import app
    print("✅ main.py imports OK")
except Exception as e:
    print(f"❌ main.py import failed: {e}")
    sys.exit(1)

print("\n✅ ALL IMPORTS SUCCESSFUL!")

# Test regex patterns
print("\nTesting regex patterns...")
patterns = get_all_patterns()
print(f"✅ Loaded {len(patterns)} detection patterns")

# Test basic regex detection
test_text = "password=hunter2 api_key=sk-prod-abc123 secret=mysecret"
findings = detect_all(test_text)
print(f"✅ Regex detection found {len(findings)} findings in test text")

# Test risk scoring
print("\nTesting risk scoring...")
test_findings = [
    {"type": "password", "risk": "critical"},
    {"type": "api_key", "risk": "high"}
]
score = calculate_risk_score(test_findings)
level = get_risk_level(score)
print(f"✅ Risk score: {score}, level: {level}")

# Test policy action
print("\nTesting policy engine...")
action = determine_action(level, {"mask": True, "block_high_risk": True})
print(f"✅ Policy action: {action}")

print("\n" + "="*50)
print("✅ BACKEND VERIFICATION COMPLETE!")
print("="*50)
