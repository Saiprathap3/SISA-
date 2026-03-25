import React, { useState } from 'react'

export default function SQLInput({ onSubmit, loading }: { onSubmit: (sql: string) => void; loading?: boolean }) {
  const [value, setValue] = useState('')

  function lineNumbers(text: string){
    return text.split('\n').map((_,i)=>i+1).join('\n')
  }

  return (
    <div className="sql-container">
      <div className="sql-line-numbers monospace">{lineNumbers(value)}</div>
      <div className="flex-1">
        <textarea value={value} onChange={e => setValue(e.target.value)} placeholder="SELECT * FROM users WHERE..." className="text-editor-main" />
        <div className="flex-between flex-center mt-8">
          <div className="muted">SQL editor — monospace</div>
          <button onClick={() => onSubmit(value)} className="accent-btn btn-with-spinner" disabled={loading}>{loading ? <span className="spinner" /> : null}Analyze SQL</button>
        </div>
      </div>
    </div>
  )
}
