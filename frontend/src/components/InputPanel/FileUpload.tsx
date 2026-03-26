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
    <div className={`dashed-drop ${drag ? 'dragging' : ''}`} onDragOver={e => e.preventDefault()} onDragEnter={() => setDrag(true)} onDragLeave={() => setDrag(false)} onDrop={handleDrop}>
      {!file ? (
        <div className="flex-col flex-gap-8 flex-center">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginBottom: '8px', filter: 'drop-shadow(0 0 8px rgba(0, 255, 198, 0.4))' }}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
          <div className="muted" style={{ fontSize: '15px', fontWeight: 500 }}>Drag & drop a file here</div>
          <div className="muted f-12">Supported: .log .txt .pdf .doc .docx .sql</div>
          <label className="accent-btn pointer" style={{ marginTop: '12px' }}>
            Browse files
            <input type="file" accept=".log,.txt,.pdf,.doc,.docx,.sql" onChange={onBrowse} className="d-none" />
          </label>
        </div>
      ) : (
        <div className="flex-between flex-center">
          <div>
            <div className="fw-700">{file.name}</div>
            <div className="muted">{(file.size/1024).toFixed(1)} KB • {file.type || 'unknown'}</div>
          </div>
          <div className="flex-gap-8">
            <button onClick={() => { handleSelect(null) }} className="accent-btn">Remove</button>
          </div>
        </div>
      )}
    </div>
  )
}
