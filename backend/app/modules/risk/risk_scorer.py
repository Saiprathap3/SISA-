from typing import List, Dict, Tuple
from .risk_engine import score_findings, score_to_level, determine_action


def compute_risk(findings: List[Dict], options: Dict) -> Tuple[int, str, str]:
    """Thin wrapper to compute score, level and action.

    Returns a tuple (score:int, level:str, action:str)
    """
    score = score_findings(findings)
    level = score_to_level(score)
    action = determine_action(level, options)
    return score, level, action
