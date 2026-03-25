import React from 'react'
import type { Finding } from '../../types'

export default function LogViewer({ text, findings }: { text: string; findings: Finding[] }) {
  const lines = text.split('\n')
  const hits = new Map<number, string>()
  findings.forEach(f => { if (f.line) hits.set(f.line, f.risk) })

  return (
    <pre className="log-viewer-pre">
      {lines.map((l, idx) => {
        const num = idx + 1
        const risk = hits.get(num)
        const riskClass = risk ? risk.toLowerCase() : ''

        return (
          <div key={idx} className={`log-viewer-line ${riskClass}`}>
            <span className="log-viewer-num">{num.toString().padStart(3, ' ')} </span>
            <span>{l}</span>
          </div>
        )
      })}
    </pre>
  )
}
