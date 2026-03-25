import React from 'react'

export default function RiskBreakdown({ counts }: { counts: Record<string, number> }) {
  // counts comes from API response detection_breakdown: { regex, statistical, ml, ai }
  const breakdown = counts ?? { regex: 0, statistical: 0, ml: 0, ai: 0 };
  const total = Math.max(
    (breakdown.regex ?? 0) + (breakdown.statistical ?? 0) + 
    (breakdown.ml ?? 0) + (breakdown.ai ?? 0), 
    1
  );

  const methods = [
    { key: 'regex', label: 'Regex', color: '#3b82f6' },
    { key: 'statistical', label: 'Statistical', color: '#8b5cf6' },
    { key: 'ml', label: 'ML', color: '#ec4899' },
    { key: 'ai', label: 'AI', color: '#14b8a6' }
  ];

  return (
    <div className="risk-breakdown-container">
      {methods.map(method => {
        const count = breakdown[method.key as keyof typeof breakdown] ?? 0;
        const percentage = total > 0 ? (count / total) * 100 : 0;
        return (
          <div key={method.key} className="breakdown-bar-wrapper" style={{ flex: 1 }}>
            <div 
              className="breakdown-bar"
              style={{
                height: `${Math.max(percentage, 5)}%`,
                backgroundColor: method.color,
                minHeight: '20px',
                borderRadius: '4px'
              }}
              title={method.label}
            />
            <div className="breakdown-label">{method.label}</div>
            <div className="breakdown-count">{count}</div>
          </div>
        );
      })}
    </div>
  );
}
