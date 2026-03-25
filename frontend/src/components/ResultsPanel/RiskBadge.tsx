import React from 'react'
import type { RiskLevel, ActionTaken } from '../../types'

export function RiskBadge({ level, score }: { level: RiskLevel; score?: number }) {
  const colorClass = `bg-${level.toLowerCase()}`
  return (
    <div className={`badge-container ${colorClass}`}>
      {level.toUpperCase()} {score ? `• ${score}` : ''}
    </div>
  )
}

export function ActionBadge({ action }: { action: ActionTaken }) {
  const colorClass = `bg-${action.toLowerCase()}`
  return (
    <div className={`badge-container ${colorClass}`}>
      {action.toUpperCase()}
    </div>
  )
}
