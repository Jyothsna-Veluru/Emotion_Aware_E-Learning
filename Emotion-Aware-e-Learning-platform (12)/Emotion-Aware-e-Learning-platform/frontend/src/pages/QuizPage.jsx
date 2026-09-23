import { useEffect, useState } from 'react'
import { api } from '../api'
import Quiz from '../components/Quiz'

export default function QuizPage() {
  const [courses, setCourses] = useState([])
  const [courseId, setCourseId] = useState('python')
  const [course, setCourse] = useState(null)
  const [moduleId, setModuleId] = useState('')
  const [emotion, setEmotion] = useState('neutral')

  useEffect(() => { api.courses().then(setCourses) }, [])
  useEffect(() => {
    api.course(courseId).then((c) => { setCourse(c); setModuleId(c.modules[0].id) })
  }, [courseId])

  return (
    <div className="max-w-3xl mx-auto px-5 py-12">
      <h1 className="text-3xl font-extrabold">Quiz practice</h1>
      <p className="text-slate-400 mt-2">Pick a module and an emotion to see how the quiz adapts its difficulty.</p>

      <div className="glass rounded-2xl p-4 mt-6 grid sm:grid-cols-3 gap-3">
        <label className="text-sm">
          <span className="text-slate-400 text-xs">Course</span>
          <select value={courseId} onChange={(e) => setCourseId(e.target.value)} className="w-full mt-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2">
            {courses.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </label>
        <label className="text-sm">
          <span className="text-slate-400 text-xs">Module</span>
          <select value={moduleId} onChange={(e) => setModuleId(e.target.value)} className="w-full mt-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2">
            {course?.modules.map((m) => <option key={m.id} value={m.id}>{m.title}</option>)}
          </select>
        </label>
        <label className="text-sm">
          <span className="text-slate-400 text-xs">Simulated emotion</span>
          <select value={emotion} onChange={(e) => setEmotion(e.target.value)} className="w-full mt-1 bg-black/30 border border-white/10 rounded-lg px-3 py-2">
            {['happy', 'sad', 'angry', 'fear', 'surprise', 'neutral'].map((e) => <option key={e} value={e}>{e}</option>)}
          </select>
        </label>
      </div>

      <div className="mt-6">
        {moduleId && <Quiz key={moduleId + emotion} courseId={courseId} moduleId={moduleId} emotion={emotion} confidence={0.9} />}
      </div>
    </div>
  )
}
