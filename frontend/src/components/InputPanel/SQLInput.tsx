import React, { useState } from 'react'

export default function SQLInput({ onSubmit, loading }: { onSubmit: (sql: string) => void; loading?: boolean }) {
  const [value, setValue] = useState('')

  function lineNumbers(text: string){
    return text.split('\n').map((_,i)=>i+1).join('\n')
  }

  return (
    <div style={{ display: 'flex', gap:8 }}>
      <div style={{ background: '#0f1318', color: '#9aa6b2', padding: 8, textAlign: 'right', userSelect: 'none', borderRadius:6, minHeight:300, paddingTop:12 }} className="monospace">{lineNumbers(value)}</div>
      <div style={{ flex:1 }}>
        <textarea value={value} onChange={e => setValue(e.target.value)} placeholder="SELECT * FROM users WHERE..." style={{ width: '100%', minHeight: 300, background: '#0b1014', color: '#e6eef8', fontFamily: 'Fira Code, IBM Plex Mono, monospace', padding: 12, borderRadius:6 }} />
        <div style={{ marginTop: 8, display:'flex', justifyContent:'space-between', alignItems:'center' }}>
          <div className="muted">SQL editor — monospace</div>
          <button onClick={() => onSubmit(value)} className="accent-btn btn-with-spinner" disabled={loading}>{loading ? <span className="spinner" /> : null}Analyze SQL</button>
        </div>
      </div>
    </div>
  )
}
