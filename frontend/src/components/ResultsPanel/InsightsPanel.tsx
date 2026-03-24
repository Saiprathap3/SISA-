import React from 'react'

export default function InsightsPanel({ insights, anomalies, aiUsed, breakdown }: { insights: string[]; anomalies: string[]; aiUsed: boolean; breakdown?: any }) {
  const bd = breakdown || { regex_findings: 0, statistical_findings: 0, ml_findings: 0, ai_findings: 0 }
  const total = Math.max(1, bd.regex_findings + bd.statistical_findings + bd.ml_findings + bd.ai_findings)
  
  function Bar({ label, count, color }: any) {
    const bars = "██████████"
    const pct = Math.round((count / total) * 10)
    return (
      <div className="bar-row">
        <div className="bar-label">{label}</div>
        <div className="bar-viz" style={{ '--bar-color': color } as React.CSSProperties}>{bars.slice(0, pct).padEnd(10, '░')}</div>
        <div className="muted">{count} findings</div>
      </div>
    )
  }

  return (
    <div className="insights-panel panel">
      <div className="insights-title">DETECTION BREAKDOWN</div>
      <div className="insights-grid">
        <Bar label="Regex" count={bd.regex_findings} color="#58a6ff" />
        <Bar label="Statistical" count={bd.statistical_findings} color="#bc8cff" />
        <Bar label="ML" count={bd.ml_findings} color="#7ee787" />
        <Bar label="AI" count={bd.ai_findings} color="#ff7b72" />
      </div>

      <div style={{ marginTop: 16 }}>
        <div className="insights-title">AI INSIGHTS {aiUsed ? '✨' : ''}</div>
        {insights && insights.length > 0 ? (
          insights.map((t, i) => <div key={i} className="insight-item">💡 {t}</div>)
        ) : (
          <div style={{ color: '#9aa6b2', fontSize: 13 }}>No AI insights available</div>
        )}
      </div>

      {anomalies && anomalies.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <div className="insights-title" style={{ color: '#f43f5e' }}>ANOMALIES</div>
          {anomalies.map((a, i) => <div key={i} className="anomaly-item">⚠️ {a}</div>)}
        </div>
      )}
    </div>
  )
}
