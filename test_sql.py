#!/usr/bin/env python3
import requests

r = requests.post('http://localhost:8000/analyze', 
    json={
        'input_type': 'sql', 
        'content': 'SELECT * FROM users WHERE 1=1; DROP TABLE users; UNION SELECT password FROM admin;', 
        'options': {'mask': True, 'block_high_risk': True, 'use_ai': False}
    }, 
    timeout=10
)
print('Status:', r.status_code)
d = r.json()
print(f'Risk: {d["risk_level"]}, Score: {d["risk_score"]}, Findings: {len(d["findings"])}')
print(f'Action: {d.get("action")}')
print(f'Summary: {d.get("summary")}')
