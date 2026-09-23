import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { emotionMeta } from '../emotions'

/**
 * TutorChat
 * ---------
 * The signature chatbot. Sends messages to /tutor-chat with the current
 * emotion + lesson context. Also surfaces IMMEDIATE interventions pushed in
 * via the `intervention` prop (fired by the parent when emotion changes).
 */
export default function TutorChat({ emotion = 'neutral', courseId, moduleTitle, intervention }) {
  const [messages, setMessages] = useState([
    { role: 'tutor', text: "Hi! I'm your AI tutor. Ask me anything about the lesson, or tell me if you're stuck.", engine: 'offline' },
  ])
  const [input, setInput] = useState('')
  const [sending, setSending] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages])

  // Immediate-response system: when a new intervention arrives, inject it.
  useEffect(() => {
    if (!intervention?.message) return
    setMessages((m) => [...m, { role: 'tutor', text: intervention.message, intervention: true, urgent: intervention.urgent }])
  }, [intervention])

  async function send() {
    const text = input.trim()
    if (!text || sending) return
    const next = [...messages, { role: 'student', text }]
    setMessages(next)
    setInput('')
    setSending(true)
    try {
      const history = next.slice(-8).map((m) => ({ role: m.role, text: m.text }))
      const reply = await api.tutorChat({ message: text, emotion, course_id: courseId, module_title: moduleTitle, history })
      setMessages((m) => [...m, reply])
    } catch (_) {
      setMessages((m) => [...m, { role: 'tutor', text: 'I had trouble reaching the server — try again in a moment.', engine: 'error' }])
    } finally {
      setSending(false)
    }
  }

  const meta = emotionMeta(emotion)

  return (
    <div className="glass rounded-2xl flex flex-col h-[460px]">
      <div className="px-4 py-3 border-b border-white/10 flex items-center gap-2">
        <span className="w-8 h-8 rounded-xl btn-grad flex items-center justify-center text-sm">🤖</span>
        <div className="flex-1">
          <div className="font-semibold text-sm">AI Tutor</div>
          <div className="text-[11px] text-slate-400">Adapting to: <span style={{ color: meta.color }}>{meta.label} {meta.emoji}</span></div>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'student' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[85%] px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed animate-slide-in ${
                m.role === 'student'
                  ? 'btn-grad text-white rounded-br-sm'
                  : m.intervention
                  ? 'bg-amber-500/15 border border-amber-400/30 text-amber-100 rounded-bl-sm'
                  : 'glass-soft text-slate-100 rounded-bl-sm'
              }`}
            >
              {m.intervention && <div className="text-[10px] uppercase tracking-wide text-amber-300/80 mb-1">⚡ Live nudge</div>}
              {m.text}
            </div>
          </div>
        ))}
        {sending && <div className="text-xs text-slate-500 pl-1 animate-pulse">Tutor is typing…</div>}
      </div>

      <div className="p-3 border-t border-white/10 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="Ask the tutor anything…"
          className="flex-1 bg-black/30 border border-white/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-indigo-400/50 transition"
        />
        <button onClick={send} disabled={sending || !input.trim()} className="btn-grad px-4 rounded-xl text-sm font-semibold text-white">
          Send
        </button>
      </div>
    </div>
  )
}
