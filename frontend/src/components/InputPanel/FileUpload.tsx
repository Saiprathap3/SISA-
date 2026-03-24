import React, { useState } from 'react'

export default function FileUpload({ onFile }: { onFile: (f: File | null) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [drag, setDrag] = useState(false)

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setDrag(false)
    const f = e.dataTransfer.files?.[0]
    if (f) handleSelect(f)
  }

  function handleSelect(f: File | null) {
    setFile(f)
    onFile(f)
  }

  function onBrowse(e: React.ChangeEvent<HTMLInputElement>){
    const f = e.target.files?.[0] ?? null
    if (f) handleSelect(f)
  }

  return (
    <div className={`dashed-drop ${drag ? 'dragging' : ''}`} onDragOver={e => e.preventDefault()} onDragEnter={() => setDrag(true)} onDragLeave={() => setDrag(false)} onDrop={handleDrop} style={{ color: '#e6eef8' }}>
      {!file ? (
        <div style={{ display:'flex', flexDirection:'column', gap:8, alignItems:'center' }}>
          <div className="muted">Drag & drop a file here</div>
          <div className="muted">Supported: .log .txt .pdf .doc .docx .sql</div>
          <label className="accent-btn" style={{ cursor:'pointer' }}>
            Browse files
            <input type="file" accept=".log,.txt,.pdf,.doc,.docx,.sql" onChange={onBrowse} style={{ display:'none' }} />
          </label>
        </div>
      ) : (
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ fontWeight:700 }}>{file.name}</div>
            <div className="muted">{(file.size/1024).toFixed(1)} KB • {file.type || 'unknown'}</div>
          </div>
          <div style={{ display:'flex', gap:8 }}>
            <button onClick={() => { handleSelect(null) }} className="accent-btn">Remove</button>
          </div>
        </div>
      )}
    </div>
  )
}
