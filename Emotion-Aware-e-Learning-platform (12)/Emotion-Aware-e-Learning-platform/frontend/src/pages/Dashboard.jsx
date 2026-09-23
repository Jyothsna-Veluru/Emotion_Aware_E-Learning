import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { emotionMeta, EMOTION_META } from '../emotions'

function Stat({ label, value, sub }) {
  return (
    <div className="glass rounded-2xl p-5">
      <div className="text-3xl font-extrabold gradient-text">{value}</div>
      <div className="text-sm text-slate-300 mt-1">{label}</div>
      {sub && <div className="text-xs text-slate-500 mt-0.5">{sub}</div>}
    </div>
  )
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => { api.progress().then(setData).finally(() => setLoading(false)) }, [])

  if (loading) return <div className="max-w-5xl mx-auto px-5 py-20 text-slate-400 animate-pulse">Loading analytics…</div>

  const a = data.analytics
  const dist = a.emotion_distribution || {}
  const totalEmotions = Object.values(dist).reduce((s, n) => s + n, 0) || 1
  const empty = a.modules_completed === 0 && a.quizzes_taken === 0 && totalEmotions <= 1

  return (
    <div className="max-w-5xl mx-auto px-5 py-12">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-extrabold">Progress dashboard</h1>
        <span className="text-xs px-2.5 py-1 rounded-full bg-white/5 text-slate-400">storage: {a.storage}</span>
      </div>

      {empty ? (
        <div className="glass rounded-2xl p-10 mt-8 text-center">
          <div className="text-4xl mb-3">📊</div>
          <p className="text-slate-300">No activity yet.</p>
          <Link to="/courses" className="btn-grad inline-block mt-4 px-5 py-2.5 rounded-xl font-semibold text-white text-sm">Start a session →</Link>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-8">
            <Stat label="Modules completed" value={a.modules_completed} />
            <Stat label="Avg quiz score" value={`${a.average_quiz_score}%`} sub={`${a.quizzes_taken} quizzes`} />
            <Stat label="Challenges passed" value={a.challenges_passed} />
            <Stat label="Dominant mood" value={emotionMeta(a.dominant_emotion).emoji} sub={emotionMeta(a.dominant_emotion).label} />
          </div>

          {/* Emotion distribution */}
          <div className="glass rounded-2xl p-6 mt-5">
            <h2 className="font-semibold mb-4">Emotional journey</h2>
            <div className="space-y-3">
              {Object.keys(EMOTION_META).map((e) => {
                const n = dist[e] || 0
                const pct = Math.round((n / totalEmotions) * 100)
                const m = emotionMeta(e)
                return (
                  <div key={e} className="flex items-center gap-3">
                    <span className="w-20 text-sm flex items-center gap-1.5">{m.emoji} {m.label}</span>
                    <div className="flex-1 h-2.5 rounded-full bg-white/10 overflow-hidden">
                      <div className="h-full rounded-full transition-all duration-700" style={{ width: `${pct}%`, background: m.color }} />
                    </div>
                    <span className="w-10 text-right text-xs text-slate-400">{pct}%</span>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Recent quizzes */}
          {data.quiz_scores?.length > 0 && (
            <div className="glass rounded-2xl p-6 mt-5">
              <h2 className="font-semibold mb-3">Recent quizzes</h2>
              <div className="space-y-2">
                {data.quiz_scores.slice(-6).reverse().map((q, i) => (
                  <div key={i} className="flex items-center justify-between text-sm glass-soft rounded-lg px-3 py-2">
                    <span className="text-slate-300">{q.course_id} · {q.module_id}</span>
                    <span className="font-semibold" style={{ color: q.score_pct >= 60 ? '#22c55e' : '#f87171' }}>{q.score_pct}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
