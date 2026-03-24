import { RiskBadge, ActionBadge } from '../ResultsPanel/RiskBadge'
import type { RiskLevel, ActionTaken } from '../../types'

function Donut({ score }: { score: number }) {
  const pct = Math.max(0, Math.min(100, score || 0))
  const color = pct > 80 ? '#f43f5e' : pct > 50 ? '#f97316' : pct > 20 ? '#f59e0b' : '#10b981'
  const radius = 30
  const circ = 2 * Math.PI * radius
  const offset = circ * (1 - pct / 100)
  
  return (
    <div style={{ position: 'relative', width: 70, height: 70, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg width="70" height="70" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r={radius} stroke="#1e2736" strokeWidth="8" fill="none" />
        <circle cx="40" cy="40" r={radius} stroke={color} strokeWidth="8" fill="none" 
          strokeDasharray={`${circ}`} strokeDashoffset={offset} strokeLinecap="round" transform="rotate(-90 40 40)" />
      </svg>
      <div style={{ position: 'absolute', fontWeight: 700, fontSize: 12, color: color }}>{pct}%</div>
    </div>
  )
}

export default function SummaryBar({ 
  level, 
  score, 
  action, 
  findingsCount, 
  duration, 
  totalLines, 
  requestId 
}: { 
  level: RiskLevel; 
  score: number; 
  action: ActionTaken; 
  findingsCount: number; 
  duration?: number; 
  totalLines?: number; 
  requestId?: string; 
}) {
  return (
    <div className="summary-grid">
      <Donut score={score} />
      <div className="stat-box">
        <div className="stat-label">Risk Level</div>
        <RiskBadge level={level} />
      </div>
      <div className="stat-box">
        <div className="stat-label">Action</div>
        <ActionBadge action={action} />
      </div>
      <div style={{ textAlign: 'right' }} className="stat-box">
        <div style={{ fontSize: 13, fontWeight: 700 }}>{findingsCount} findings</div>
        <div className="muted" style={{ fontSize: 10 }}>
          {duration ? `${Math.round(duration)}ms` : ''} 
          {totalLines ? ` • ${totalLines} lines` : ''}
        </div>
        <div className="muted" style={{ fontSize: 10 }}>{requestId?.slice(0, 8)}</div>
      </div>
    </div>
  )
}


