import React from 'react'

export default function Header({ onMenuToggle, onLogsToggle }: { onMenuToggle?: () => void; onLogsToggle?: () => void }) {
  return (
    <header className="glass-header header-main">
      <button 
        className="hamburger-btn"
        onClick={onMenuToggle}
        aria-label="Toggle navigation menu"
        aria-expanded="false"
      >
        ☰
      </button>
      <div className="header-logo-container">
        <div className="header-logo-icon">🔰</div>
        <div>
          <div className="header-title">SecureAI <span className="muted fw-500">Intelligence Platform</span></div>
          <div className="f-12 muted">v1.0</div>
        </div>
      </div>
      <div className="header-status">
        <button 
          className="header-log-btn"
          onClick={onLogsToggle}
          title="View system logs"
          aria-label="View live system logs"
        >
          📊 Logs
        </button>
        <div className="status-dot" />
        <div className="muted">System Online</div>
      </div>
    </header>
  )
}
