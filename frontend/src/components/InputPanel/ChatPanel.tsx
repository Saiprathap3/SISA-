import React, { useState, useRef, useEffect } from 'react'

type Msg = { role: 'user' | 'ai'; text: string }

export default function ChatPanel({ onSend }: { onSend?: (text:string)=>Promise<void> }){
  const [messages, setMessages] = useState<Msg[]>([])
  const [input, setInput] = useState('')
  const boxRef = useRef<HTMLDivElement|null>(null)

  async function send(){
    if(!input.trim()) return
    const msg:Msg = { role:'user', text: input }
    setMessages(prev=>[...prev,msg])
    setInput('')
    if(onSend){
      try{ await onSend(input) }catch{}
    }
  }

  useEffect(()=>{ if(boxRef.current) boxRef.current.scrollTop = boxRef.current.scrollHeight }, [messages])

  return (
    <div style={{ display:'flex', flexDirection:'column', gap:8, height:'100%' }}>
      <div ref={boxRef} style={{ flex:1, overflowY:'auto', padding:12, background:'#081018', borderRadius:8 }}>
        {messages.length===0 && <div className="muted">No messages yet. Start the conversation.</div>}
        {messages.map((m,i)=>(
          <div key={i} style={{ marginBottom:8 }}>
            <div style={{ fontSize:12, color:'#9aa6b2' }}>{m.role === 'user' ? 'User' : 'AI'}</div>
            <div style={{ background: m.role==='user' ? '#0b6cff' : '#0b1220', color: m.role==='user' ? '#081018' : '#e6eef8', padding:8, borderRadius:6, display:'inline-block', marginTop:4 }}>{m.text}</div>
          </div>
        ))}
      </div>
      <div style={{ display:'flex', gap:8, alignItems:'center' }}>
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder="Type a message..." style={{ flex:1, padding:8, borderRadius:6, background:'#0b1014', color:'#e6eef8', border:'1px solid rgba(255,255,255,0.02)' }} />
        <button className="accent-btn" onClick={send}>Send</button>
      </div>
    </div>
  )
}
