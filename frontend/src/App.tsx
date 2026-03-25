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
import type { InputType, AnalyzeOptions } from './types'


export default function App() {
  const [selectedType, setSelectedType] = useState<'text' | 'file' | 'sql' | 'log' | 'chat'>('text')
  const [options, setOptions] = useState({ mask: true, log_analysis: true, block_high_risk: true })
  const { result, loading, error, analyze, analyzeFile } = useAnalyze()
  const [originalContent, setOriginalContent] = useState('')

  async function handleFile(f: File | null) {
    if (!f) return
    try {
      setOriginalContent(`File: ${f.name} (${(f.size / 1024).toFixed(1)} KB)`)
      await analyzeFile(f, options)
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

  async function handleAnalysis(text: string, type: InputType) {
    setOriginalContent(text)
    await analyze(text, type, options)
  }

  const exportJSON = () => {
    if (!result) return
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `secureai-report-${result.request_id || 'export'}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
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
    a.href = url
    a.download = `secureai-report-${result.request_id || 'export'}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
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
      {loading && <div className="top-progress w-full" />}
      <Header />
      <div className="flex">
        <Sidebar selectedType={selectedType} onTypeChange={setSelectedType} options={options} onOptionsChange={setOptions} />
        <main className="flex-1 p-20">
          <div className="grid-main">
            <section>
              {selectedType === 'text' && <TextInput onSubmit={(t) => handleAnalysis(t, 'text')} loading={loading} />}
              {selectedType === 'file' && <FileUpload onFile={handleFile} />}
              {selectedType === 'sql' && <SQLInput loading={loading} onSubmit={(t) => handleAnalysis(t, 'sql')} />}
              {selectedType === 'log' && <LogUpload onFile={handleLogFile} onPaste={(t) => handleAnalysis(t, 'log')} />}
              {selectedType === 'chat' && <ChatPanel onSend={(t) => handleAnalysis(t, 'chat')} />}
              
              {error && <div className="error-alert">⚠️ {error}</div>}
              
              {selectedType === 'log' && result && (
                 <div className="mt-24">
                   <div className="fw-700 mb-8">LOG VIEWER</div>
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
                totalLines={result?.total_lines_analyzed}
                requestId={result?.request_id}
                summary={result?.summary}
              />
              <div className="mt-12">
                <FindingsCard findings={result?.findings || []} onExportJSON={exportJSON} onExportCSV={exportCSV} onCopySummary={copySummary} />
                <InsightsPanel insights={result?.insights || []} anomalies={result?.anomalies} breakdown={result?.detection_breakdown} />
              </div>
            </aside>
          </div>
        </main>
      </div>
    </div>
  )
}

