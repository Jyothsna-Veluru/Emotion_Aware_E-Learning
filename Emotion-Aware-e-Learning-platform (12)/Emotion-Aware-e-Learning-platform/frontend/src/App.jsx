import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import NavBar from './components/NavBar'
import Landing from './pages/Landing'
import CourseSelect from './pages/CourseSelect'
import LearningSession from './pages/LearningSession'
import QuizPage from './pages/QuizPage'
import Dashboard from './pages/Dashboard'
import { api } from './api'

export default function App() {
  const [health, setHealth] = useState(null)
  const [offline, setOffline] = useState(false)

  useEffect(() => {
    api.health().then(setHealth).catch(() => setOffline(true))
  }, [])

  return (
    <div className="min-h-full flex flex-col">
      <NavBar />

      {/* Only show a banner when the backend is completely unreachable */}
      {offline && (
        <div className="bg-red-500/15 border-b border-red-400/30 text-center text-sm py-2 text-red-200">
          ⚠️ Backend not reachable. Start it with <code className="font-mono">python app.py</code> in the <code className="font-mono">backend/</code> folder.
        </div>
      )}

      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/courses" element={<CourseSelect />} />
          <Route path="/learn/:courseId" element={<LearningSession />} />
          <Route path="/quiz" element={<QuizPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>

      <footer className="border-t border-white/10 py-6 text-center text-xs text-slate-500">
        Emotion-Aware e-Learning Platform · AI · Computer Vision · Adaptive Education
      </footer>
    </div>
  )
}