import { useCallback, useEffect, useRef, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api'
import { emotionMeta } from '../emotions'
import Webcam from '../components/Webcam'
import TutorChat from '../components/TutorChat'
import Quiz from '../components/Quiz'
import Challenge from '../components/Challenge'

export default function LearningSession() {
  const { courseId } = useParams()
  const [course, setCourse]         = useState(null)
  const [idx, setIdx]               = useState(0)
  const [emotion, setEmotion]       = useState('neutral')
  const [confidence, setConfidence] = useState(1)
  const [directive, setDirective]   = useState(null)
  const [intervention, setIntervention] = useState(null)
  const [tab, setTab]               = useState('lesson')

  // Refs so callbacks never go stale without recreating
  const lastEmotionRef   = useRef('neutral')
  const adaptingRef      = useRef(false)   // prevent overlapping adaptive API calls

  useEffect(() => { api.course(courseId).then(setCourse) }, [courseId])

  /**
   * handleEmotion is called by Webcam ONLY when the emotion or confidence
   * has meaningfully changed (Webcam handles the deduplication).
   * We still guard with adaptingRef so two rapid changes don't stack calls.
   */
  const handleEmotion = useCallback(async (result) => {
    // Update visible state immediately (no flicker — just label/confidence bar)
    setEmotion(result.emotion)
    setConfidence(result.confidence)

    if (adaptingRef.current) return
    adaptingRef.current = true

    try {
      const emotionChanged = result.emotion !== lastEmotionRef.current

      const [dir, interv] = await Promise.all([
        api.adaptiveResponse(result.emotion, result.confidence),
        emotionChanged
          ? api.intervention(result.emotion, result.confidence)
          : Promise.resolve(null),
      ])

      setDirective(dir)
      if (interv) setIntervention({ ...interv, _ts: Date.now() })
      lastEmotionRef.current = result.emotion
    } catch (_) {
      // ignore — keep last directive
    } finally {
      adaptingRef.current = false
    }
  }, []) // stable ref — no dependency on changing state

  if (!course) return (
    <div className="max-w-6xl mx-auto px-5 py-20 text-slate-400 animate-pulse">Loading session…</div>
  )

  const module      = course.modules[idx]
  const meta        = emotionMeta(emotion)
  const exampleKey  = directive?.example || 'basic'
  const exampleText = module.examples[exampleKey] || module.examples.basic

  async function completeModule() {
    await api.completeModule(module.id)
    if (idx < course.modules.length - 1) { setIdx(idx + 1); setTab('lesson') }
  }

  return (
    <div className="max-w-6xl mx-auto px-5 py-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div>
          <Link to="/courses" className="text-xs text-slate-400 hover:text-white">← All courses</Link>
          <h1 className="text-2xl font-extrabold mt-1">{course.name}</h1>
        </div>
        <div className="text-right">
          <div className="text-xs text-slate-400">Module {idx + 1} of {course.modules.length}</div>
          <div className="w-40 h-1.5 mt-1 rounded-full bg-white/10 overflow-hidden">
            <div className="h-full btn-grad rounded-full transition-all"
              style={{ width: `${((idx + 1) / course.modules.length) * 100}%` }} />
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-5">
        {/* LEFT: webcam + adaptation card + tutor */}
        <div className="space-y-5">
          {/* Slower interval + Webcam only fires onEmotion on real changes */}
          <Webcam onEmotion={handleEmotion} intervalMs={10000} />

          {directive && (
            <div
              className="glass rounded-2xl p-4 transition-all duration-500"
              style={{ borderColor: meta.color + '40' }}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xl">{meta.emoji}</span>
                <span className="text-sm font-semibold" style={{ color: meta.color }}>{meta.label} detected</span>
              </div>
              <p className="text-sm text-slate-200">{directive.headline}</p>
              <ul className="mt-2 space-y-1">
                {directive.actions.map((a, i) => (
                  <li key={i} className="text-xs text-slate-400 flex items-center gap-1.5">
                    <span style={{ color: directive.accent }}>●</span> {a}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <TutorChat emotion={emotion} courseId={courseId} moduleTitle={module.title} intervention={intervention} />
        </div>

        {/* RIGHT: lesson / quiz / challenge */}
        <div className="lg:col-span-2 space-y-5">
          <div className="glass rounded-2xl p-1.5 flex gap-1">
            {['lesson', 'quiz', 'challenge'].map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`flex-1 py-2 rounded-xl text-sm font-medium capitalize transition ${
                  tab === t ? 'btn-grad text-white' : 'text-slate-300 hover:bg-white/5'
                }`}
              >
                {t === 'lesson' ? '📘 Lesson' : t === 'quiz' ? '❓ Quiz' : '⚡ Challenge'}
              </button>
            ))}
          </div>

          {tab === 'lesson' && (
            <div className="glass rounded-2xl p-6">
              <h2 className="text-xl font-bold">{module.title}</h2>
              <p className="text-slate-300 mt-3 leading-relaxed">{module.explanation}</p>

              <div className="mt-5">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-slate-200">Example</h3>
                  <span className="text-[11px] px-2 py-0.5 rounded-full bg-white/5 text-slate-400 capitalize">
                    {exampleKey} (adapted to {emotion})
                  </span>
                </div>
                <pre className="code-block">{exampleText}</pre>
              </div>

              <div className="mt-5 glass-soft rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-200 mb-1">✏️ Practice task</h3>
                <p className="text-sm text-slate-300">{module.practice_task}</p>
              </div>

              {directive?.show_bonus && (
                <div className="mt-4 rounded-xl p-4 border border-green-400/30 bg-green-400/10">
                  <h3 className="text-sm font-semibold text-green-300 mb-1">🎁 Bonus challenge unlocked</h3>
                  <p className="text-sm text-slate-200">
                    You're doing great — try the advanced example without running it, then check the coding challenge tab.
                  </p>
                </div>
              )}

              <div className="flex gap-2 mt-6">
                <button disabled={idx === 0} onClick={() => setIdx(idx - 1)}
                  className="px-4 py-2 rounded-xl glass-soft text-sm disabled:opacity-40">
                  ← Previous
                </button>
                <button onClick={completeModule}
                  className="btn-grad px-5 py-2 rounded-xl text-sm font-semibold text-white ml-auto">
                  {idx < course.modules.length - 1 ? 'Complete & next →' : '✓ Finish course'}
                </button>
              </div>
            </div>
          )}

          {tab === 'quiz' && (
            <Quiz courseId={courseId} moduleId={module.id} emotion={emotion} confidence={confidence} />
          )}

          {tab === 'challenge' && (
            <Challenge challenge={module.challenge} language={courseId} />
          )}
        </div>
      </div>
    </div>
  )
}