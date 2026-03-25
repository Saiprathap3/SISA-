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
    <div className="chat-box">
      <div ref={boxRef} className="chat-messages">
        {messages.length===0 && <div className="muted">No messages yet. Start the conversation.</div>}
        {messages.map((m,i)=>(
          <div key={i} className="mb-8">
            <div className="f-12 muted">{m.role === 'user' ? 'User' : 'AI'}</div>
            <div className={`chat-msg-bubble ${m.role==='user' ? 'chat-msg-user' : 'chat-msg-ai'}`}>{m.text}</div>
          </div>
        ))}
      </div>
      <div className="flex-gap-8 flex-center">
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder="Type a message..." className="flex-1 p-12 br-6 bg-dark color-white border-subtle" />
        <button className="accent-btn" onClick={send}>Send</button>
      </div>
    </div>
  )
}
