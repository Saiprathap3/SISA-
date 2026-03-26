import React, { useEffect, useRef, useState } from 'react'
import { streamLogs, getLogHistory } from '../../services/api'
import type { Finding, LiveLogEntry } from '../../types'

interface LogViewerProps {
  text?: string
  findings?: Finding[]
  isLive?: boolean
  onClose?: () => void
}

export default function LogViewer({ text, findings = [], isLive = false, onClose }: LogViewerProps) {
  // For file analysis mode
  if (!isLive && text) {
    return <FileLogViewer text={text} findings={findings} />
  }

  // For live stream mode
  return <LiveStreamViewer onClose={onClose} />
}

function FileLogViewer({ text, findings }: { text: string; findings: Finding[] }) {
  const lines = text.split('\n')
  const findingLines = new Set(findings.map(f => f.line).filter(Boolean))
  const riskOrder: Record<string, number> = { critical: 4, high: 3, medium: 2, low: 1, none: 0 }

  return (
    <pre className="log-viewer-pre">
      {lines.map((l, idx) => {
        const lineNumber = idx + 1
        const hasFindings = findingLines.has(lineNumber)
        const findingsOnLine = findings.filter(f => f.line === lineNumber)
        const highestRisk = findingsOnLine.reduce((max, finding) => {
          const currentRisk = (finding.risk || 'none').toLowerCase()
          return (riskOrder[currentRisk] || 0) > (riskOrder[max] || 0) ? currentRisk : max
        }, 'none')
        const riskClass = hasFindings ? highestRisk : ''

        return (
          <div key={idx} className={`log-viewer-line ${riskClass}`}>
            <span className="log-viewer-num">{lineNumber.toString().padStart(3, ' ')} </span>
            <span>{l}</span>
          </div>
        )
      })}
    </pre>
  )
}

function LiveStreamViewer({ onClose }: { onClose?: () => void }) {
  const [logs, setLogs] = useState<LiveLogEntry[]>([])
  const [filter, setFilter] = useState('')
  const [isPaused, setIsPaused] = useState(false)
  const [loading, setLoading] = useState(true)
  const containerRef = useRef<HTMLDivElement>(null)
  const unsubscribeRef = useRef<(() => void) | null>(null)

  const MAX_LOGS = 200

  useEffect(() => {
    // Load initial history
    getLogHistory()
      .then(history => {
        setLogs(history.slice(-MAX_LOGS))
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load log history:', err)
        setLoading(false)
      })

    // Subscribe to live stream
    if (!isPaused) {
      unsubscribeRef.current = streamLogs(
        (entry) => {
          setLogs(prev => {
            const updated = [...prev, entry].slice(-MAX_LOGS)
            // Auto-scroll
            setTimeout(() => {
              if (containerRef.current) {
                containerRef.current.scrollTop = containerRef.current.scrollHeight
              }
            }, 0)
            return updated
          })
        },
        (error) => console.error('Log stream error:', error)
      )
    }

    return () => {
      unsubscribeRef.current?.()
    }
  }, [isPaused])

  const filteredLogs = filter
    ? logs.filter(log =>
        log.message.toLowerCase().includes(filter.toLowerCase()) ||
        log.level.toLowerCase().includes(filter.toLowerCase())
      )
    : logs

  const levelColor = (level: string): string => {
    const l = level.toUpperCase()
    return {
      INFO: '#10b981',
      DEBUG: '#8b5cf6',
      WARN: '#f59e0b',
      ERROR: '#ef4444',
    }[l] || '#e6eef8'
  }

  return (
    <div className="live-log-viewer">
      <div className="live-log-header">
        <div className="live-log-title">📊 Live System Logs</div>
        <div className="live-log-controls">
          <input
            type="text"
            placeholder="Search logs..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
            className="live-log-search"
          />
          <button
            onClick={() => setIsPaused(!isPaused)}
            className="live-log-btn"
            title={isPaused ? 'Resume' : 'Pause'}
          >
            {isPaused ? '▶️ Resume' : '⏸️ Pause'}
          </button>
          <button
            onClick={() => setLogs([])}
            className="live-log-btn"
            title="Clear logs"
          >
            🗑️ Clear
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="live-log-btn live-log-close"
              title="Close"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      <div className="live-log-container" ref={containerRef}>
        {loading && <div className="live-log-loading">Loading logs...</div>}
        {!loading && filteredLogs.length === 0 && (
          <div className="live-log-empty">No logs to display</div>
        )}
        {filteredLogs.map((log, idx) => (
          <div
            key={idx}
            className="live-log-entry"
            style={{ borderLeftColor: levelColor(log.level) }}
          >
            <div className="live-log-meta">
              <span
                className="live-log-level"
                style={{
                  backgroundColor: levelColor(log.level),
                  color: log.level === 'INFO' || log.level === 'DEBUG' ? '#000' : '#fff',
                }}
              >
                {log.level}
              </span>
              <span className="live-log-time">
                {new Date(log.timestamp).toLocaleTimeString()}
              </span>
              {log.status_code && (
                <span
                  className="live-log-status"
                  style={{
                    color: log.status_code >= 500 ? '#ef4444' : log.status_code >= 400 ? '#f59e0b' : '#10b981',
                  }}
                >
                  {log.method} {log.path} • {log.status_code}
                </span>
              )}
            </div>
            <div className="live-log-message">{log.message}</div>
            {log.response_time_ms && (
              <div className="live-log-details">
                ⏱️ {log.response_time_ms}ms {log.ip && `• IP: ${log.ip}`}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="live-log-footer">{filteredLogs.length} of {logs.length} logs</div>
    </div>
  )
}
