import { Link, useLocation } from 'react-router-dom'

export default function NavBar() {
  const { pathname } = useLocation()
  const links = [
    { to: '/', label: 'Home' },
    { to: '/courses', label: 'Courses' },
    { to: '/dashboard', label: 'Dashboard' },
  ]
  return (
    <header className="sticky top-0 z-40">
      <nav className="glass border-b border-white/10">
        <div className="max-w-6xl mx-auto px-5 h-14 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2.5 font-bold">
            <img src="/brain.svg" alt="" className="w-7 h-7" />
            <span className="hidden sm:inline">Emotion-Aware <span className="gradient-text">e-Learning</span></span>
          </Link>
          <div className="flex items-center gap-1">
            {links.map((l) => (
              <Link
                key={l.to}
                to={l.to}
                className={`px-3.5 py-1.5 rounded-lg text-sm transition ${
                  pathname === l.to ? 'bg-white/10 text-white' : 'text-slate-300 hover:text-white hover:bg-white/5'
                }`}
              >
                {l.label}
              </Link>
            ))}
          </div>
        </div>
      </nav>
    </header>
  )
}
