// Shared emotion metadata used across the UI.
export const EMOTION_META = {
  happy:    { label: 'Happy',    emoji: '😊', color: '#22c55e', glow: 'rgba(34,197,94,0.5)' },
  sad:      { label: 'Sad',      emoji: '😢', color: '#60a5fa', glow: 'rgba(96,165,250,0.5)' },
  angry:    { label: 'Angry',    emoji: '😠', color: '#f87171', glow: 'rgba(248,113,113,0.5)' },
  fear:     { label: 'Fear',     emoji: '😨', color: '#a78bfa', glow: 'rgba(167,139,250,0.5)' },
  surprise: { label: 'Surprise', emoji: '😲', color: '#fbbf24', glow: 'rgba(251,191,36,0.5)' },
  neutral:  { label: 'Neutral',  emoji: '😐', color: '#94a3b8', glow: 'rgba(148,163,184,0.5)' },
}

export const emotionMeta = (e) => EMOTION_META[e] || EMOTION_META.neutral
