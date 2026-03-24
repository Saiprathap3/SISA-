from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PolicyConfig:
    block_on_critical: bool = True
    mask_high_risk: bool = True
    allow_low_risk: bool = True
    alert_on_brute_force: bool = True


@dataclass
class PolicyDecision:
    action: str
    reasons: List[str]
    alerts: List[str]


def evaluate(findings: List[Dict], anomalies: List[str], options: Dict) -> PolicyDecision:
    """Evaluate policy against findings and anomalies and return a decision."""
    cfg = PolicyConfig(
        block_on_critical=options.get("block_on_critical", True),
        mask_high_risk=options.get("mask_output", True),
        allow_low_risk=True,
        alert_on_brute_force=True,
    )
    reasons: List[str] = []
    alerts: List[str] = []

    has_critical = any(f.get("risk") == "critical" for f in findings)
    has_high_medium = any(f.get("risk") in ("high", "medium") for f in findings)

    if has_critical and cfg.block_on_critical:
        reasons.append("critical findings present and block_on_critical")
        action = "blocked"
    elif has_high_medium and cfg.mask_high_risk:
        reasons.append("masking high/medium risk findings")
        action = "masked"
    elif not findings:
        action = "allowed"
    else:
        action = "allowed"

    if anomalies and cfg.alert_on_brute_force:
        alerts.extend(anomalies)

    return PolicyDecision(action=action, reasons=reasons, alerts=alerts)
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PolicyConfig:
    block_on_critical: bool = True
    mask_high_risk: bool = True
    allow_low_risk: bool = True
    alert_on_brute_force: bool = True


@dataclass
class PolicyDecision:
    action: str
    reasons: List[str]
    alerts: List[str]


def evaluate(findings: List[Dict], anomalies: List[str], options: Dict) -> PolicyDecision:
    cfg = PolicyConfig(
        block_on_critical=options.get("block_on_critical", True),
        mask_high_risk=options.get("mask_high_risk", True),
        allow_low_risk=options.get("allow_low_risk", True),
        alert_on_brute_force=options.get("alert_on_brute_force", True),
    )
    reasons: List[str] = []
    alerts: List[str] = []

    risks = {f.get("risk") for f in findings}
    if "critical" in risks and cfg.block_on_critical:
        reasons.append("critical finding present")
        action = "blocked"
        if anomalies and cfg.alert_on_brute_force:
            alerts.extend(anomalies)
        return PolicyDecision(action=action, reasons=reasons, alerts=alerts)

    if ("high" in risks or "medium" in risks) and cfg.mask_high_risk:
        reasons.append("high/medium findings masked")
        action = "masked"
    elif not findings:
        reasons.append("no findings")
        action = "allowed"
    else:
        action = "allowed"

    if anomalies and cfg.alert_on_brute_force:
        alerts.extend(anomalies)

    return PolicyDecision(action=action, reasons=reasons, alerts=alerts)
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PolicyConfig:
    block_on_critical: bool = True
    mask_high_risk: bool = True
    allow_low_risk: bool = True
    alert_on_brute_force: bool = True


@dataclass
class PolicyDecision:
    action: str
    reasons: List[str]
    alerts: List[str]


def evaluate(findings: List[Dict], anomalies: List[str], options: Dict) -> PolicyDecision:
    """Evaluate findings and anomalies against policy configuration.

    `options` overrides defaults. Returns a PolicyDecision.
    """
    cfg = PolicyConfig(
        block_on_critical=options.get("block_on_critical", True),
        mask_high_risk=options.get("mask_high_risk", options.get("mask_output", True)),
        allow_low_risk=options.get("allow_low_risk", True),
        alert_on_brute_force=options.get("alert_on_brute_force", True),
    )

    reasons: List[str] = []
    alerts: List[str] = []

    has_critical = any(f.get("risk") == "critical" for f in findings)
    has_high_medium = any(f.get("risk") in ("high", "medium") for f in findings)

    if has_critical and cfg.block_on_critical:
        reasons.append("critical findings present and block_on_critical")
        action = "blocked"
    elif has_high_medium and cfg.mask_high_risk:
        reasons.append("masking high/medium risk findings")
        action = "masked"
    elif not findings:
        reasons.append("no findings")
        action = "allowed"
    else:
        action = "allowed"

    if anomalies and cfg.alert_on_brute_force:
        alerts.extend(anomalies)

    return PolicyDecision(action=action, reasons=reasons, alerts=alerts)
