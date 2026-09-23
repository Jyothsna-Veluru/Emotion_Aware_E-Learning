import { Link } from 'react-router-dom'
import { EMOTION_META } from '../emotions'

const FEATURES = [
  { icon: '🎥', title: 'Real-time emotion sensing', desc: 'Your webcam reads facial expressions every few seconds using DeepFace + OpenCV.' },
  { icon: '🧠', title: 'Adaptive learning', desc: 'Lessons, examples and quiz difficulty shift the moment your emotion changes.' },
  { icon: '🤖', title: 'AI tutor chatbot', desc: 'An emotion-aware tutor explains, motivates and answers questions in context.' },
  { icon: '⚡', title: 'Immediate response system', desc: 'Frustrated or anxious? The platform intervenes instantly with a nudge or a breather.' },
  { icon: '🧩', title: 'Coding challenges', desc: 'Hands-on Python & Java challenges with hints and progress tracking.' },
  { icon: '📊', title: 'Learning analytics', desc: 'Track completed modules, quiz scores and your emotional journey over time.' },
]

export default function Landing() {
  return (
    <div className="max-w-6xl mx-auto px-5">
      {/* Hero */}
      <section className="pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 text-xs px-3 py-1.5 rounded-full glass-soft mb-6 animate-fade-up">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" /> AI · Computer Vision · Adaptive Education
        </div>
        <h1 className="text-4xl sm:text-6xl font-extrabold leading-tight animate-fade-up">
          Learning that <span className="gradient-text">feels</span> how you feel
        </h1>
        <p className="mt-5 text-lg text-slate-300 max-w-2xl mx-auto animate-fade-up">
          An AI-powered platform that detects your emotions through the webcam and adapts lessons,
          quizzes and tutoring in real time — so studying meets you where you are.
        </p>
        <div className="mt-8 flex items-center justify-center gap-3 animate-fade-up">
          <Link to="/courses" className="btn-grad px-6 py-3 rounded-xl font-semibold text-white">Start learning →</Link>
          <Link to="/dashboard" className="px-6 py-3 rounded-xl glass-soft font-semibold hover:bg-white/5 transition">View dashboard</Link>
        </div>

        {/* Emotion strip */}
        <div className="mt-12 flex flex-wrap items-center justify-center gap-3 animate-fade-up">
          {Object.entries(EMOTION_META).map(([k, m]) => (
            <div key={k} className="glass-soft rounded-xl px-4 py-2 flex items-center gap-2 animate-float" style={{ animationDelay: `${Math.random()}s` }}>
              <span className="text-xl">{m.emoji}</span>
              <span className="text-sm" style={{ color: m.color }}>{m.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="pb-24">
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {FEATURES.map((f, i) => (
            <div key={i} className="glass rounded-2xl p-5 hover:-translate-y-1 transition animate-fade-up" style={{ animationDelay: `${i * 0.05}s` }}>
              <div className="text-3xl mb-3">{f.icon}</div>
              <h3 className="font-semibold mb-1">{f.title}</h3>
              <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
