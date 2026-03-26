import React from 'react'

export default function Header({ onMenuToggle, onLogsToggle, action = 'allowed' }: { onMenuToggle?: () => void; onLogsToggle?: () => void, action?: string }) {
  const isAtRisk = action === 'blocked';
  return (
    <header className="glass-header header-main" style={{ position: 'sticky', top: 0, zIndex: 1000 }}>
      <button 
        className="hamburger-btn"
        onClick={onMenuToggle}
        aria-label="Toggle navigation menu"
        aria-expanded="false"
      >
        ☰
      </button>
      <div className="header-logo-container">
        <div className="header-logo-icon" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="cyber-shield"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        </div>
        <div>
          <div className="header-title" style={{ fontSize: '18px', color: 'var(--text-main)', textShadow: '0 0 10px rgba(0, 255, 198, 0.3)' }}>
            AI Secure Data Intelligence Platform
          </div>
          <div className="f-12 muted" style={{ color: 'var(--accent)', marginTop: '2px', fontWeight: 500 }}>
            Real-Time Log Security Analyzer
          </div>
        </div>
      </div>
      <div className="header-status">
        <div className={`system-status ${isAtRisk ? 'at-risk' : ''}`}>
          <div className="system-status-dot" />
          {isAtRisk ? 'System Status: At Risk' : 'System Status: Secure'}
        </div>
        <button 
          className="header-log-btn"
          onClick={onLogsToggle}
          title="View system logs"
          aria-label="View live system logs"
        >
          <span style={{ marginRight: '6px' }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ verticalAlign: 'middle' }}><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
          </span>
          SOC Logs
        </button>
      </div>
    </header>
  )
}
