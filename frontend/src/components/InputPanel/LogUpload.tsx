import React, { useState, useRef, ChangeEvent } from 'react'

interface LogUploadProps {
  onFile: (f: File | null) => void;
  onPaste?: (text: string) => void;
}

export default function LogUpload({ onFile, onPaste }: LogUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [paste, setPaste] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] ?? null
    if (f && (f.name.toLowerCase().endsWith('.log') || f.name.toLowerCase().endsWith('.txt'))) {
      updateFile(f)
    } else if (f) {
      alert('Please upload a .log or .txt file')
      e.target.value = '' // Clear the input
    }
  }

  const updateFile = (f: File | null) => {
    setFile(f)
    onFile(f)
    if (f) setPaste('')
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const f = e.dataTransfer.files?.[0] ?? null
    if (f && (f.name.toLowerCase().endsWith('.log') || f.name.toLowerCase().endsWith('.txt'))) {
      updateFile(f)
    } else if (f) {
      alert('Please upload a .log or .txt file')
    }
  }

  const handlePasteSubmit = () => {
    if (onPaste && paste.trim()) {
      onPaste(paste)
      updateFile(null)
    }
  }

  const lineCount = paste.trim() 
    ? paste.split(/\r?\n/).length 
    : (file ? Math.max(1, Math.floor(file.size / 80)) : 0)

  return (
    <div className="log-upload-container animate-fade-in">
      <div 
        className={`dashed-drop ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input 
          type="file" 
          ref={fileInputRef}
          accept=".log,.txt" 
          onChange={handleFileChange} 
          onClick={(e) => e.stopPropagation()}
          className="d-none"
          aria-label="Log file upload"
        />
        
        {!file ? (
          <div 
            className="upload-drop-zone clickable-zone"
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                fileInputRef.current?.click();
              }
            }}
            aria-label="Upload log file"
          >
            <div className="upload-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            <div className="text-center">
              <div className="fw-600 f-15">Drop log file here or click to browse</div>
              <div className="muted f-13 mt-4">Supports .log and .txt files</div>
            </div>
          </div>
        ) : (
          <div className="file-row">
            <div className="file-details">
              <div className="file-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              </div>
              <div>
                <div className="fw-700 f-14">{file.name}</div>
                <div className="muted f-12">
                  {(file.size / 1024).toFixed(1)} KB • approx {lineCount} lines
                </div>
              </div>
            </div>
            <button 
              className="accent-btn" 
              onClick={(e) => { e.stopPropagation(); updateFile(null); }}
            >
              Remove
            </button>
          </div>
        ) }
      </div>
      
      <div className="panel">
        <div className="paste-header">
          <div className="fw-700 f-14">Or paste raw log text</div>
          {paste.trim() && <div className="muted f-12">{lineCount} lines detected</div>}
        </div>
        <textarea 
          className="log-paste-area monospace f-13"
          value={paste} 
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => { 
            setPaste(e.target.value); 
            if (file) updateFile(null); 
          }} 
          placeholder="Paste logs here standard logs or security events..." 
          aria-label="Raw log text"
        />
        <div className="flex-end mt-12">
          <button 
            className="accent-btn analyze-btn" 
            onClick={handlePasteSubmit} 
            disabled={!paste.trim() || !onPaste}
          >
            Analyze Pasted Content
          </button>
        </div>
      </div>
    </div>
  )
}


