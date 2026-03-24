import React from 'react'

export default function RiskBreakdown({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + (b || 0), 0) || 1
  const colors: Record<string, string> = { critical: '#b91c1c', high: '#f97316', medium: '#f59e0b', low: '#16a34a' }
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', height: 60 }}>
      {(['critical', 'high', 'medium', 'low'] as string[]).map(k => (
        <div key={k} style={{ width: 40, background: '#071018', display: 'flex', alignItems: 'flex-end', justifyContent: 'center' }}>
          <div style={{ width: '80%', height: `${(counts[k] || 0) / total * 100}%`, background: colors[k], transition: 'height 300ms' }} />
        </div>
      ))}
    </div>
  )
}
