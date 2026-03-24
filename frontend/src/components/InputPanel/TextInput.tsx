import React, { useState, useEffect, useRef } from 'react'

export default function TextInput({ onSubmit, loading, placeholder = 'Enter text here...' }: { onSubmit: (text: string) => void; loading?: boolean; placeholder?: string }) {
  const [value, setValue] = useState('')
  const ref = useRef<HTMLTextAreaElement | null>(null)

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === 'Enter') {
        onSubmit(value)
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [value, onSubmit])

  return (
    <div>
      <textarea ref={ref} value={value} onChange={e => setValue(e.target.value)} placeholder={placeholder} style={{ width: '100%', minHeight: 300, background: '#141920', color: '#e6eef8', fontFamily: 'IBM Plex Mono, monospace', padding: 12, borderRadius: 6, border: '1px solid #1e2736' }} />
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
        <div style={{ color: '#9aa6b2' }}>{value.length} chars</div>
        <button onClick={() => onSubmit(value)} disabled={loading} style={{ background: '#0b6cff', color: 'white', padding: '8px 16px', borderRadius: 6 }}>{loading ? 'Analyzing...' : 'Analyze'}</button>
      </div>
    </div>
  )
}

