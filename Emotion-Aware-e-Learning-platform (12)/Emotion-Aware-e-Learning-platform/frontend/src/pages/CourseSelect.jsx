import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'

export default function CourseSelect() {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const nav = useNavigate()

  useEffect(() => {
    api.courses().then(setCourses).finally(() => setLoading(false))
  }, [])

  return (
    <div className="max-w-5xl mx-auto px-5 py-14">
      <h1 className="text-3xl font-extrabold">Choose a course</h1>
      <p className="text-slate-400 mt-2">Pick a track to begin an emotion-aware study session.</p>

      {loading ? (
        <p className="mt-10 text-slate-400 animate-pulse">Loading courses…</p>
      ) : (
        <div className="grid sm:grid-cols-2 gap-5 mt-8">
          {courses.map((c, i) => (
            <button
              key={c.id}
              onClick={() => nav(`/learn/${c.id}`)}
              className="text-left glass rounded-2xl p-6 hover:-translate-y-1 transition group animate-fade-up"
              style={{ animationDelay: `${i * 0.06}s` }}
            >
              <div className="flex items-center justify-between">
                <span className="w-12 h-12 rounded-2xl flex items-center justify-center text-2xl font-bold"
                  style={{ background: c.color + '22', color: c.color }}>
                  {c.id === 'python' ? '🐍' : '☕'}
                </span>
                <span className="text-xs px-2.5 py-1 rounded-full bg-white/5 text-slate-300">{c.module_count} modules</span>
              </div>
              <h3 className="text-xl font-bold mt-4">{c.name}</h3>
              <p className="text-sm text-slate-400 mt-1">{c.tagline}</p>
              <div className="mt-4 text-sm font-semibold flex items-center gap-1 group-hover:gap-2 transition-all" style={{ color: c.color }}>
                Start session →
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
