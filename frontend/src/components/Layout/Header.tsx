import React from 'react'

export default function Header() {
  return (
    <header className="glass-header" style={{ height: 64, borderBottom: '1px solid rgba(255,255,255,0.03)', display: 'flex', alignItems: 'center', padding: '0 20px', color: '#e6eef8' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
        <div style={{ width: 40, height: 40, background: 'linear-gradient(90deg,#58a6ff,#0b6cff)', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 6px 18px rgba(11,108,255,0.12)' }}>🔰</div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 16 }}>SecureAI <span style={{ color: 'var(--muted)', fontWeight: 500 }}>Intelligence Platform</span></div>
          <div style={{ fontSize: 12, color: '#9aa6b2' }}>v1.0</div>
        </div>
      </div>
      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 14 }}>
        <div style={{ width: 10, height: 10, background: '#12b76a', borderRadius: 99 }} />
        <div style={{ color: '#9aa6b2' }}>System Online</div>
      </div>
    </header>
  )
}
