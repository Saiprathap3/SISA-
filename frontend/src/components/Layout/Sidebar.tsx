import React from 'react'
import type { InputType } from '../../types'

const types: { key: InputType; label: string; emoji: string }[] = [
  { key: 'text', label: 'Text', emoji: '📝' },
  { key: 'file', label: 'File', emoji: '📁' },
  { key: 'sql', label: 'SQL', emoji: '🗄' },
  { key: 'log', label: 'Log', emoji: '📋' },
  { key: 'chat', label: 'Chat', emoji: '💬' },
]

export default function Sidebar({ selectedType, onTypeChange, options, onOptionsChange }: { selectedType: InputType; onTypeChange: (t: InputType) => void; options: any; onOptionsChange: (o: any) => void }) {
  return (
    <aside style={{ width: 260, background: 'var(--panel)', color: '#e6eef8', padding: 16, height: '100vh', boxSizing: 'border-box' }}>
      <div style={{ marginBottom: 12, fontWeight: 700 }}>Input Type</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {types.map(t => (
          <button key={t.key} onClick={() => onTypeChange(t.key)} className={`tab-button ${selectedType === t.key ? 'active' : ''}`} style={{ textAlign: 'left', display:'flex', gap:8, alignItems:'center' }}>
            <span style={{ marginRight: 8 }}>{t.emoji}</span>
            {t.label}
          </button>
        ))}
      </div>

      <div style={{ marginTop: 20, fontWeight: 700 }}>Options</div>
      <div style={{ marginTop: 8, display:'grid', gap:12 }}>
        <div className="tooltip" data-tip="Mask sensitive fields in results">
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
            <div>Mask Output</div>
            <div className="toggle">
              <div className={`switch ${options.mask_output ? 'on' : ''}`} onClick={()=>onOptionsChange({ ...options, mask_output: !options.mask_output })}><div className="knob" /></div>
            </div>
          </div>
        </div>

        <div className="tooltip" data-tip="Use AI models for deeper analysis">
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
            <div>Use AI</div>
            <div className="toggle">
              <div className={`switch ${options.use_ai ? 'on' : ''}`} onClick={()=>onOptionsChange({ ...options, use_ai: !options.use_ai })}><div className="knob" /></div>
            </div>
          </div>
        </div>

        {options.use_ai && (
          <div style={{ display:'flex', flexDirection:'column', gap:6 }}>
            <label style={{ fontSize:12, color:'var(--muted)' }}>Model</label>
            <select value={options.model || 'gpt4o'} onChange={e => onOptionsChange({ ...options, model: e.target.value })} style={{ padding:8, borderRadius:6, background:'#0b1014', color:'#e6eef8', border:'1px solid rgba(255,255,255,0.02)' }}>
              <option value="gpt4o">GPT-4o</option>
              <option value="claude">Claude</option>
              <option value="gemini">Gemini</option>
              <option value="local">Local / Ollama</option>
            </select>
          </div>
        )}

        <div className="tooltip" data-tip="Block processing when critical findings are present">
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
            <div>Block Critical</div>
            <div className="toggle">
              <div className={`switch ${options.block_on_critical ? 'on' : ''}`} onClick={()=>onOptionsChange({ ...options, block_on_critical: !options.block_on_critical })}><div className="knob" /></div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
