import React from 'react'

export default function InsightsPanel({ insights, anomalies, breakdown }: { insights: string[]; anomalies?: string[]; breakdown?: any }) {
  const bd = breakdown ?? { regex: 0, statistical: 0, ml: 0, ai: 0 };
  const total = Math.max(1, (bd.regex ?? 0) + (bd.statistical ?? 0) + (bd.ml ?? 0) + (bd.ai ?? 0));
  
  // Determine if AI insights are from Claude (ai count > 0) or fallback
  const isClaudeInsights = (bd.ai ?? 0) > 0;

  // Color determination based on count
  const getBarColor = (method: string, count: number): string => {
    if (count === 0) return '#666666'; // dim gray for 0 findings
    
    const colorMap: Record<string, { medium: string; bright: string }> = {
      regex: { medium: '#3b82f6', bright: '#0b6cff' },
      statistical: { medium: '#8b5cf6', bright: '#a78bfa' },
      ml: { medium: '#ec4899', bright: '#f472b6' },
      ai: { medium: '#14b8a6', bright: '#2dd4bf' }
    };
    
    const colors = colorMap[method] || colorMap.regex;
    return count >= 3 ? colors.bright : colors.medium;
  };

  const methods = [
    { key: 'regex', label: 'Regex', color: '#3b82f6' },
    { key: 'statistical', label: 'Statistical', color: '#8b5cf6' },
    { key: 'ml', label: 'ML', color: '#ec4899' },
    { key: 'ai', label: 'AI', color: '#14b8a6' }
  ];

  return (
    <div className="insights-panel panel">
      <div className="insights-title">DETECTION BREAKDOWN</div>
      <div className="insights-grid">
        {methods.map(method => {
          const count = bd[method.key] ?? 0;
          const barColor = getBarColor(method.key, count);
          const filledDots = count > 0 ? Math.max(1, Math.round((count / total) * 20)) : 0;
          const totalDots = 20;
          return (
            <div key={method.key} className="bar-row">
              <div className="bar-label">{method.label}</div>
              <div className="bar-viz" style={{ color: barColor }}>
                {'█'.repeat(filledDots)}{'░'.repeat(Math.max(0, totalDots - filledDots))}
              </div>
              <div>{count} findings</div>
            </div>
          );
        })}
      </div>

      <div className="mt-16">
        <div className="insights-title">AI INSIGHTS</div>
        {insights && insights.length > 0 ? (
          <>
            <div style={{ marginBottom: '12px', fontSize: '12px', color: '#666' }}>
              {isClaudeInsights ? '🤖 Powered by Claude' : '📋 Rule-based insights'}
            </div>
            {insights.map((t, i) => <div key={i} className="insight-item">💡 {t}</div>)}
          </>
        ) : (
          <div className="muted f-13">No insights available</div>
        )}
      </div>

      {anomalies && anomalies.length > 0 && (
        <div className="mt-16">
          <div className="insights-title alert-text">ANOMALIES</div>
          {anomalies.map((a, i) => <div key={i} className="anomaly-item">⚠️ {a}</div>)}
        </div>
      )}
    </div>
  )
}
