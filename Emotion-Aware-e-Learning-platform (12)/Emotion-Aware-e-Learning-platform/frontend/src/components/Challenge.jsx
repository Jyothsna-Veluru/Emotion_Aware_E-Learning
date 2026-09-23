import { useEffect, useState } from 'react'
import { api } from '../api'

/**
 * Challenge
 * ---------
 * Shows a coding challenge with a starter, a reveal-able hint, an editable
 * code area, and a "mark complete" flow that records the result to /progress.
 * (Code is not executed server-side for safety; the student self-verifies
 * against the hint, mirroring how interview-style practice tools work.)
 */
export default function Challenge({ challenge, language = 'python', onComplete }) {
  const [code, setCode] = useState(challenge?.starter || '')
  const [showHint, setShowHint] = useState(false)
  const [done, setDone] = useState(false)

  useEffect(() => { setCode(challenge?.starter || ''); setShowHint(false); setDone(false) }, [challenge])

  if (!challenge) return null

  async function mark(passed) {
    await api.submitChallenge({ challenge_title: challenge.title, passed })
    setDone(true)
    onComplete?.(passed)
  }

  return (
    <div className="glass rounded-2xl p-5">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold flex items-center gap-2">⚡ Challenge: {challenge.title}</h3>
        <span className="text-[11px] px-2 py-1 rounded-full bg-white/5 text-slate-300 uppercase">{language}</span>
      </div>

      <p className="text-sm text-slate-300 mb-3">{challenge.prompt}</p>

      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
        className="code-block w-full h-44 outline-none resize-y focus:border-indigo-400/50"
      />

      <div className="flex flex-wrap gap-2 mt-3">
        <button onClick={() => setShowHint((s) => !s)} className="text-sm px-3 py-2 rounded-lg glass-soft hover:border-indigo-400/40 border border-transparent transition">
          {showHint ? 'Hide hint' : '💡 Show hint'}
        </button>
        {!done ? (
          <button onClick={() => mark(true)} className="btn-grad text-sm px-4 py-2 rounded-lg font-semibold text-white ml-auto">
            ✓ I solved it
          </button>
        ) : (
          <span className="ml-auto text-sm text-green-400 self-center">Recorded — nice work! 🎉</span>
        )}
      </div>

      {showHint && (
        <div className="mt-3 text-sm glass-soft rounded-xl p-3 text-amber-100/90 animate-fade-up">
          💡 {challenge.hint}
        </div>
      )}
    </div>
  )
}
