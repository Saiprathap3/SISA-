import { useState } from 'react'
import Header from './components/Layout/Header'
import Sidebar from './components/Layout/Sidebar'
import TextInput from './components/InputPanel/TextInput'
import FileUpload from './components/InputPanel/FileUpload'
import SQLInput from './components/InputPanel/SQLInput'
import LogUpload from './components/InputPanel/LogUpload'
import ChatPanel from './components/InputPanel/ChatPanel'
import FindingsCard from './components/ResultsPanel/FindingsCard'
import InsightsPanel from './components/ResultsPanel/InsightsPanel'
import LogViewer from './components/ResultsPanel/LogViewer'
import SummaryBar from './components/Dashboard/SummaryBar'
import { useAnalyze } from './hooks/useAnalyze'

export default function App() {
  const [selectedType, setSelectedType] = useState<'text' | 'file' | 'sql' | 'log' | 'chat'>('text')
  const [options, setOptions] = useState({ mask_output: true, use_ai: true, block_on_critical: true })
  const { result, loading, error, analyze, analyzeFile } = useAnalyze()
  const [originalContent, setOriginalContent] = useState('')

  async function handleFile(f: File | null) {
    if (!f) return
    try {
      const res = await analyzeFile(f, options)
      setOriginalContent(res?.summary || '') 
    } catch (e) { console.error(e) }
  }

  async function handleLogFile(f: File | null) {
    if (!f) return
    try {
      const text = await f.text()
      setOriginalContent(text)
      await analyze(text, 'log', options)
    } catch (e) { console.error(e) }
  }

  async function handleAnalysis(text: string, type: string) {
    setOriginalContent(text)
    await analyze(text, type, options)
  }

  const exportJSON = () => {
    if (!result) return
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = 'secureai-report.json'; a.click()
  }

  const exportCSV = () => {
    if (!result) return
    let csv = "line,finding_type,risk_level,detection_method,masked_value,recommendation\n"
    result.findings.forEach((f) => {
      csv += `"${f.line || '-'}","${f.type}","${f.risk}","${f.detection_method || 'regex'}","${f.masked_value || f.original_line || ''}","${f.recommendation || ''}"\n`
    })
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = 'secureai-report.csv'; a.click()
  }

  async function copySummary() {
    if (!result) return
    let text = `=== SECUREAI ANALYSIS ===\nRisk: ${result.risk_level}\nFindings: ${result.findings.length}\n`
    result.findings.slice(0, 5).forEach((f) => {
      text += `[${f.risk}] Line ${f.line || '-'} — ${f.type} (${f.masked_value || f.value || 'Redacted'})\n`
    })
    await navigator.clipboard.writeText(text)
    alert('Summary copied to clipboard')
  }

  return (
    <div className="app-root">
      {loading && <div className="top-progress" style={{ width: loading ? '100%' : '0' }} />}
      <Header />
      <div style={{ display: 'flex' }}>
        <Sidebar selectedType={selectedType} onTypeChange={setSelectedType} options={options} onOptionsChange={setOptions} />
        <main style={{ flex: 1, padding: 20 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 420px', gap: 16 }}>
            <section>
              {selectedType === 'text' && <TextInput onSubmit={(t) => handleAnalysis(t, 'text')} loading={loading} />}
              {selectedType === 'file' && <FileUpload onFile={handleFile} />}
              {selectedType === 'sql' && <SQLInput loading={loading} onSubmit={(t) => handleAnalysis(t, 'sql')} />}
              {selectedType === 'log' && <LogUpload onFile={handleLogFile} onPaste={(t) => handleAnalysis(t, 'log')} />}
              {selectedType === 'chat' && <ChatPanel onSend={(t) => handleAnalysis(t, 'chat')} />}
              
              {error && <div style={{ background: '#2a0b0b', color: '#f43f5e', padding: 12, borderRadius: 8, marginTop: 16, border: '1px solid #f43f5e' }}>⚠️ {error}</div>}
              
              {selectedType === 'log' && result && (
                 <div style={{ marginTop: 24 }}>
                   <div style={{ fontWeight: 700, marginBottom: 8 }}>LOG VIEWER</div>
                   <LogViewer text={originalContent} findings={result.findings || []} />
                 </div>
              )}
            </section>
            <aside>
              <SummaryBar
                level={result?.risk_level || 'LOW'}
                score={result?.risk_score || 0}
                action={result?.action || 'allowed'}
                findingsCount={result?.findings?.length || 0}
                duration={result?.duration_ms}
                totalLines={result?.total_lines}
                requestId={result?.request_id}
              />
              <div style={{ marginTop: 12 }}>
                <FindingsCard findings={result?.findings || []} onExportJSON={exportJSON} onExportCSV={exportCSV} onCopySummary={copySummary} />
                <InsightsPanel insights={result?.insights || []} anomalies={result?.anomalies || []} aiUsed={result?.ai_used || false} breakdown={result?.detection_breakdown} />
              </div>
            </aside>
          </div>
        </main>
      </div>
    </div>
  )
}

