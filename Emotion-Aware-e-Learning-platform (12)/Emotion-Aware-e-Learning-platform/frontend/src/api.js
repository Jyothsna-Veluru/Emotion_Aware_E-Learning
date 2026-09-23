import axios from 'axios'

// In dev, Vite proxies /api -> http://localhost:5000 (see vite.config.js).
// Override with VITE_API_BASE if your backend lives elsewhere.
const BASE = import.meta.env.VITE_API_BASE || '/api'

const client = axios.create({ baseURL: BASE, timeout: 20000 })

// Stable per-browser user id so progress persists across sessions.
function userId() {
  let id = localStorage.getItem('eal_user')
  if (!id) {
    id = 'user_' + Math.random().toString(36).slice(2, 9)
    localStorage.setItem('eal_user', id)
  }
  return id
}

export const api = {
  health: () => client.get('/health').then((r) => r.data),

  courses: () => client.get('/courses').then((r) => r.data.courses),

  course: (id) => client.get(`/course/${id}`).then((r) => r.data),

  analyzeEmotion: (imageB64) =>
    client.post('/analyze-emotion', { image: imageB64, user: userId() }).then((r) => r.data),

  adaptiveResponse: (emotion, confidence) =>
    client.post('/adaptive-response', { emotion, confidence }).then((r) => r.data),

  intervention: (emotion, confidence) =>
    client.post('/intervention', { emotion, confidence }).then((r) => r.data.intervention),

  tutorChat: (payload) =>
    client.post('/tutor-chat', { ...payload, user: userId() }).then((r) => r.data),

  quiz: (payload) =>
    client.post('/quiz', payload).then((r) => r.data),

  submitQuiz: (payload) =>
    client.post('/submit-quiz', { ...payload, user: userId() }).then((r) => r.data),

  submitChallenge: (payload) =>
    client.post('/submit-challenge', { ...payload, user: userId() }).then((r) => r.data),

  completeModule: (module_id) =>
    client.post('/complete-module', { module_id, user: userId() }).then((r) => r.data),

  progress: () =>
    client.get('/progress', { params: { user: userId() } }).then((r) => r.data),
}

export { userId }
