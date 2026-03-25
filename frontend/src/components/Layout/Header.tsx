import React from 'react'

export default function Header() {
  return (
    <header className="glass-header header-main">
      <div className="header-logo-container">
        <div className="header-logo-icon">🔰</div>
        <div>
          <div className="header-title">SecureAI <span className="muted fw-500">Intelligence Platform</span></div>
          <div className="f-12 muted">v1.0</div>
        </div>
      </div>
      <div className="header-status">
        <div className="status-dot" />
        <div className="muted">System Online</div>
      </div>
    </header>
  )
}
