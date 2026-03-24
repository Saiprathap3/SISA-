import React from 'react'
import type { Finding } from '../../types'

export default function LogViewer({ text, findings }: { text: string; findings: Finding[] }) {
  const lines = text.split('\n')
  const hits = new Map<number, string>()
  findings.forEach(f => { if (f.line) hits.set(f.line, f.risk) })

  const riskColors: Record<string, string> = {
    CRITICAL: '#b91c1c',
    HIGH: '#f97316',
    MEDIUM: '#f59e0b',
    LOW: '#16a34a'
  }

  return (
    <pre className="log-viewer-pre">
      {lines.map((l, idx) => {
        const num = idx + 1
        const risk = hits.get(num)
        const styles = risk ? ({ 
          '--line-color': riskColors[risk], 
          '--line-bg': `${riskColors[risk]}11` 
        } as React.CSSProperties) : {}

        return (
          <div key={idx} className="log-viewer-line" style={styles}>
            <span className="log-viewer-num">{num.toString().padStart(3, ' ')} </span>
            <span>{l}</span>
          </div>
        )
      })}
    </pre>
  )
}
