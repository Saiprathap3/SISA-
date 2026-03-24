import { useState } from 'react'

export default function LogUpload({ onFile, onPaste }: { onFile: (f: File | null) => void; onPaste?: (text: string) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [paste, setPaste] = useState('')

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0] ?? null
    setFile(f)
    onFile(f)
    if (f) setPaste('')
  }

  function handlePasteSubmit() {
    if (onPaste && paste.trim()) {
      onPaste(paste)
      setFile(null)
    }
  }

  const lineCount = paste.trim() 
    ? paste.split(/\r?\n/).length 
    : (file ? Math.max(1, Math.floor(file.size / 80)) : 0)

  return (
    <div className="log-upload-container">
      <div className="dashed-drop" style={{ padding: 12 }}>
        {!file ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div className="muted">Upload .log or .txt file</div>
            <input type="file" accept=".log,.txt" onChange={handleChange} />
          </div>
        ) : (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 700 }}>{file.name}</div>
              <div className="muted">
                {(file.size / 1024).toFixed(1)} KB • approx {lineCount} lines
              </div>
            </div>
            <button className="accent-btn" onClick={() => { setFile(null); onFile(null); }}>Remove</button>
          </div>
        ) }
      </div>
      
      <div className="panel">
        <div style={{ fontWeight: 700, marginBottom: 8 }}>Or paste raw log text</div>
        <textarea 
          className="log-paste-area"
          value={paste} 
          onChange={e => { setPaste(e.target.value); if (file) { setFile(null); onFile(null); } }} 
          placeholder="Paste logs here..." 
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8 }}>
          <div className="muted">Lines: {lineCount}</div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button className="accent-btn" onClick={handlePasteSubmit} disabled={!paste.trim()}>Use Pasted</button>
          </div>
        </div>
      </div>
    </div>
  )
}


