import type { Finding } from '../../types'

function riskStyle(risk: string){
  const r = (risk||'').toUpperCase()
  if(r === 'CRITICAL') return { border: '1px solid #b91c1c', boxShadow: '0 0 10px rgba(185, 28, 28, 0.2)' }
  if(r === 'HIGH') return { border: '1px solid #f97316' }
  if(r === 'MEDIUM') return { border: '1px solid #f59e0b' }
  return { border: '1px solid #16a34a' }
}

function methodBadge(method: string){
  const m = (method||'regex').toUpperCase()
  const map: Record<string, string> = { REGEX: '#58a6ff', STATISTICAL: '#bc8cff', ML: '#7ee787', AI: '#ff7b72' }
  return <span style={{ fontSize:10, padding:'2px 6px', borderRadius:4, background: map[m]||'#30363d', color:'white', marginLeft:8 }}>{m}</span>
}

interface FindingsCardProps {
  findings: Finding[];
  onExportJSON: () => void;
  onExportCSV: () => void;
  onCopySummary: () => void;
}

export default function FindingsCard({ findings, onExportJSON, onExportCSV, onCopySummary }: FindingsCardProps) {
  if (!findings || findings.length === 0) return <div className="panel" style={{ padding: 16, color: '#9aa6b2' }}>✅ No findings detected</div>
  
  return (
    <div style={{ display:'flex', flexDirection:'column', gap:12 }}>
      <div style={{ display:'flex', gap:8 }}>
         <button className="accent-btn" onClick={onExportJSON} style={{ fontSize:12 }}>JSON</button>
         <button className="accent-btn" onClick={onExportCSV} style={{ fontSize:12 }}>CSV</button>
         <button className="accent-btn" onClick={onCopySummary} style={{ fontSize:12 }}>Copy Summary</button>
      </div>
      <div className="findings-list">
        {findings.map((f, i) => (
          <div key={i} style={riskStyle(f.risk)} className="finding-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
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

