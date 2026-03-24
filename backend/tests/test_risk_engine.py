from app.modules.risk.risk_engine import score_findings, score_to_level, determine_action


def test_risk_scoring_and_levels_and_actions():
    assert score_findings([]) == 0
    assert score_to_level(0) == "low"

    assert score_findings([{"risk": "critical"}]) == 4
    assert score_to_level(4) == "medium"

    assert score_findings([{"risk": "critical"}, {"risk": "high"}]) == 7
    assert score_to_level(7) == "high"

    assert score_findings([{"risk": "critical"}, {"risk": "critical"}, {"risk": "critical"}]) == 12
    assert score_to_level(12) == "critical"

    # actions
    assert determine_action("critical", {"block_on_critical": True, "mask_output": True}) == "blocked"
    assert determine_action("high", {"block_on_critical": True, "mask_output": True}) == "masked"
    assert determine_action("low", {"block_on_critical": False, "mask_output": False}) == "allowed"
