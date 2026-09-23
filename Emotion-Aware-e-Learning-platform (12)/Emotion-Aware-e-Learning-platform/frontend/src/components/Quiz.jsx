import { useEffect, useState } from 'react'
import { api } from '../api'

const DIFF_COLOR = { easy: '#22c55e', medium: '#fbbf24', hard: '#f87171' }

/**
 * Quiz
 * ----
 * Loads an emotion-adapted quiz for a module, lets the student answer, then
 * grades via /submit-quiz and shows a breakdown.
 */
export default function Quiz({ courseId, moduleId, emotion = 'neutral', confidence = 1, onGraded }) {
  const [quiz, setQuiz] = useState(null)
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let alive = true
    setLoading(true); setResult(null); setAnswers({})
    api.quiz({ course_id: courseId, module_id: moduleId, emotion, confidence })
      .then((q) => alive && setQuiz(q))
      .finally(() => alive && setLoading(false))
    return () => { alive = false }
    // re-fetch when module changes; emotion captured at load time
  }, [courseId, moduleId]) // eslint-disable-line

  async function submit() {
    const res = await api.submitQuiz({ course_id: courseId, module_id: moduleId, emotion, confidence, answers })
    setResult(res)
    onGraded?.(res)
  }

  if (loading) return <div className="glass rounded-2xl p-6 text-sm text-slate-400 animate-pulse">Building an adapted quiz…</div>
  if (!quiz) return <div className="glass rounded-2xl p-6 text-sm text-slate-400">No quiz available.</div>

  return (
    <div className="glass rounded-2xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Quiz</h3>
        <span className="text-[11px] px-2 py-1 rounded-full bg-white/5 text-slate-300">
          Adapted to <b className="capitalize">{quiz.adapted_to}</b> · targets <b>{quiz.target_difficulty}</b>
        </span>
      </div>

      <div className="space-y-4">
        {quiz.questions.map((q) => (
          <div key={q.id} className="glass-soft rounded-xl p-4">
            <div className="flex items-start justify-between gap-3">
              <p className="text-sm font-medium">{q.q}</p>
              <span className="text-[10px] uppercase px-1.5 py-0.5 rounded shrink-0" style={{ background: DIFF_COLOR[q.difficulty] + '22', color: DIFF_COLOR[q.difficulty] }}>
                {q.difficulty}
              </span>
            </div>
            <div className="grid sm:grid-cols-2 gap-2 mt-3">
              {q.options.map((opt, oi) => {
                const chosen = answers[q.id] === oi
                const graded = result?.breakdown?.find((b) => b.index === q.id)
                let cls = 'border-white/10 hover:border-indigo-400/40'
                if (result && graded) {
                  if (oi === graded.correct_answer) cls = 'border-green-400/60 bg-green-400/10'
                  else if (chosen) cls = 'border-red-400/60 bg-red-400/10'
                } else if (chosen) cls = 'border-indigo-400/70 bg-indigo-400/10'
                return (
                  <button
                    key={oi}
                    disabled={!!result}
                    onClick={() => setAnswers((a) => ({ ...a, [q.id]: oi }))}
                    className={`text-left text-sm px-3 py-2 rounded-lg border transition ${cls}`}
                  >
                    {opt}
                  </button>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      {!result ? (
        <button
          onClick={submit}
          disabled={Object.keys(answers).length < quiz.questions.length}
          className="btn-grad mt-4 w-full py-2.5 rounded-xl font-semibold text-white text-sm"
        >
          Submit quiz
        </button>
      ) : (
        <div className="mt-4 text-center glass-soft rounded-xl p-4 animate-fade-up">
          <div className="text-3xl font-bold gradient-text">{result.score_pct}%</div>
          <p className="text-sm text-slate-300 mt-1">
            {result.correct}/{result.total} correct — {result.passed ? '🎉 Passed!' : 'Review and try again'}
          </p>
        </div>
      )}
    </div>
  )
}