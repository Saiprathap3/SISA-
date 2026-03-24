import numpy as np
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest

def extract_features_per_ip(parsed_lines: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Extract numerical features from parsed log lines per IP."""
    ip_stats = {}
    
    for entry in parsed_lines:
        ip = entry.get("extra", {}).get("ip")
        if not ip:
            continue
            
        status = str(entry.get("extra", {}).get("status", ""))
        size = int(entry.get("extra", {}).get("size", 0))
        path = entry.get("extra", {}).get("path", "")
        
        if ip not in ip_stats:
            ip_stats[ip] = {
                "request_count": 0,
                "error_status_count": 0,
                "4xx_count": 0,
                "5xx_count": 0,
                "total_size": 0,
                "unique_paths": set()
            }
            
        stats = ip_stats[ip]
        stats["request_count"] += 1
        stats["total_size"] += size
        if path:
            stats["unique_paths"].add(path)
            
        if status.startswith("4") or status.startswith("5"):
            stats["error_status_count"] += 1
            if status.startswith("4"):
                stats["4xx_count"] += 1
            if status.startswith("5"):
                stats["5xx_count"] += 1
                
    # Final aggregation
    final_features = {}
    for ip, s in ip_stats.items():
        # Feature vector: [requests_per_minute, error_rate, unique_paths_accessed, avg_response_size, status_4xx, status_5xx]
        # Since we don't have total 'minutes' accurately, using raw counts or scaled
        # If total lines < 50, user said don't run.
        denominator = float(s["request_count"]) if s["request_count"] > 0 else 1.0
        final_features[ip] = [
            s["request_count"],
            s["error_status_count"] / denominator,
            len(s["unique_paths"]),
            s["total_size"] / denominator,
            s["4xx_count"],
            s["5xx_count"]
        ]
        
    return final_features

def detect_ml_anomlies(parsed_lines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Use IsolationForest to detect IP behavior anomalies."""
    if len(parsed_lines) < 50:
        return []
        
    ip_features_map = extract_features_per_ip(parsed_lines)
    if not ip_features_map:
        return []
        
    ips = list(ip_features_map.keys())
    data = np.array(list(ip_features_map.values()))
    
    if len(ips) < 2:
        return []
        
    try:
        clf = IsolationForest(
            contamination=0.01,
            n_estimators=100,
            random_state=42
        )
        # IsolationForest uses -1 for anomaly, 1 for normal
        # decision_function returns float score where negative is more anomalous
        clf.fit(data)
        scores = clf.decision_function(data)
        
        anomalies = []
        for i, score in enumerate(scores):
            # Map to risk: score < -0.5 → HIGH, score < -0.3 → MEDIUM
            risk = None
            if score < -0.5:
                risk = "high"
            elif score < -0.3:
                risk = "medium"
            
            if risk:
                anomalies.append({
                    "ip": ips[i],
                    "anomaly_score": round(float(score), 4),
                    "risk": risk,
                    "type": "ml_anomaly_detected",
                    "detection_method": "ml"
                })
        return anomalies
    except Exception:
        return []
