import React from 'react'
import type { Finding } from '../../types'

function riskClassName(risk: string){
  const r = (risk||'').toUpperCase()
  if(r === 'CRITICAL') return 'risk-critical'
  if(r === 'HIGH') return 'risk-high'
  if(r === 'MEDIUM') return 'risk-medium'
  return 'risk-low'
}

function methodBadge(method: string){
  const m = (method||'regex').toUpperCase()
  const colorClass = `bg-${m.toLowerCase()}`
  return <span className={`method-badge ${colorClass}`}>{m}</span>
}

interface FindingsCardProps {
  findings: Finding[];
  onExportJSON: () => void;
  onExportCSV: () => void;
  onCopySummary: () => void;
}

export default function FindingsCard({ findings, onExportJSON, onExportCSV, onCopySummary }: FindingsCardProps) {
  if (!findings || findings.length === 0) return <div className="panel empty-findings">✅ No findings detected</div>
  
  return (
    <div className="findings-container">
      <div className="findings-actions">
         <button className="accent-btn" onClick={onExportJSON}>JSON</button>
         <button className="accent-btn" onClick={onExportCSV}>CSV</button>
         <button className="accent-btn" onClick={onCopySummary}>Copy Summary</button>
      </div>
      <div className="findings-list">
        {findings.map((f, i) => (
          <div key={i} className={`finding-card ${riskClassName(f.risk)}`}>
            <div className="finding-card-header">
              <div>
                <span className="finding-type">{f.type.replace(/_/g, ' ').toUpperCase()}</span>
                {methodBadge(f.detection_method || 'regex')}
              </div>
              <div className="muted finding-line">Line {f.line ?? '-'}</div>
            </div>
            <div className="finding-value">
              {f.masked_value || f.value || f.original_line || 'No details'}
            </div>
            {f.recommendation && (
              <div className="finding-rec">
                💡 {f.recommendation}
              </div>
            )}
          </div>
        ))}

      </div>
    </div>
  )
}

