import React from 'react'
import type { RiskLevel, ActionTaken } from '../../types'

export function RiskBadge({ level, score }: { level: RiskLevel; score?: number }) {
  const map: Record<RiskLevel, string> = { 
    CRITICAL: '#b91c1c', 
    HIGH: '#f97316', 
    MEDIUM: '#f59e0b', 
    LOW: '#16a34a' 
  }
  return (
    <div className="badge-container" style={{ '--bg-color': map[level] } as React.CSSProperties}>
      {level.toUpperCase()} {score ? `• ${score}` : ''}
    </div>
  )
}

export function ActionBadge({ action }: { action: ActionTaken }) {
  const map: Record<ActionTaken, string> = { blocked: '#ef4444', masked: '#f59e0b', allowed: '#10b981' }
  return (
    <div className="badge-container" style={{ '--bg-color': map[action] } as React.CSSProperties}>
      {action.toUpperCase()}
    </div>
  )
}
