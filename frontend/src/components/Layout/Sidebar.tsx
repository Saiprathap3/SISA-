import { InputType, AnalyzeOptions } from '../../types'

const types: { key: InputType; label: string; emoji: string }[] = [
  { key: 'text', label: 'Text', emoji: '📝' },
  { key: 'file', label: 'File', emoji: '📁' },
  { key: 'sql', label: 'SQL', emoji: '🗄' },
  { key: 'log', label: 'Log', emoji: '📋' },
  { key: 'chat', label: 'Chat', emoji: '💬' },
]

export default function Sidebar({ selectedType, onTypeChange, options, onOptionsChange }: { selectedType: InputType; onTypeChange: (t: InputType) => void; options: AnalyzeOptions & { model?: string }; onOptionsChange: (o: AnalyzeOptions & { model?: string }) => void }) {
  return (
    <aside className="sidebar-main">
      <div className="sidebar-section-title">Input Type</div>
      <div className="sidebar-type-list">
        {types.map(t => (
          <button key={t.key} onClick={() => onTypeChange(t.key)} className={`tab-button ${selectedType === t.key ? 'active' : ''} text-left flex flex-gap-8 flex-center`}>
            <span className="mr-8">{t.emoji}</span>
            {t.label}
          </button>
        ))}
      </div>

      <div className="mt-24 fw-700">Options</div>
      <div className="sidebar-options-grid">
        <div className="tooltip" data-tip="Mask sensitive fields in results">
          <div className="sidebar-option-row">
            <div>Mask Output</div>
            <div className="toggle">
              <div className={`switch ${options.mask ? 'on' : ''}`} onClick={()=>onOptionsChange({ ...options, mask: !options.mask })}><div className="knob" /></div>
            </div>
          </div>
        </div>

        <div className="tooltip" data-tip="Use AI models for deeper analysis">
          <div className="sidebar-option-row">
            <div>Use AI</div>
            <div className="toggle">
              <div className={`switch ${options.log_analysis ? 'on' : ''}`} onClick={()=>onOptionsChange({ ...options, log_analysis: !options.log_analysis })}><div className="knob" /></div>
            </div>
          </div>
        </div>

        <div className="flex-col flex-gap-8">
          <span className="model-label">Model</span>
          <span className="model-badge">
            🤖 Powered by claude-sonnet-4-6
          </span>
        </div>

        <div className="tooltip" data-tip="Block processing when critical findings are present">
          <div className="sidebar-option-row">
            <div>Block Critical</div>
            <div className="toggle">
              <div className={`switch ${options.block_high_risk ? 'on' : ''}`} onClick={()=>onOptionsChange({ ...options, block_high_risk: !options.block_high_risk })}><div className="knob" /></div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
