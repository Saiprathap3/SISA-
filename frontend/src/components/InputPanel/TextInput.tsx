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
      <textarea ref={ref} value={value} onChange={e => setValue(e.target.value)} placeholder={placeholder} className="text-editor-main" />
      <div className="flex-between mt-8">
        <div className="muted">{value.length} chars</div>
        <button onClick={() => onSubmit(value)} disabled={loading} className="accent-btn">{loading ? 'Analyzing...' : 'Analyze'}</button>
      </div>
    </div>
  )
}

