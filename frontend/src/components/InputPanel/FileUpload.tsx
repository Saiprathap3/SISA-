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
          <div className="muted">Drag & drop a file here</div>
          <div className="muted">Supported: .log .txt .pdf .doc .docx .sql</div>
          <label className="accent-btn pointer">
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
