import { useEffect, useRef, useState } from 'react'
import { api } from '../api'
import { emotionMeta } from '../emotions'

/**
 * Webcam — smoothed emotion sampling
 * ------------------------------------
 * Captures a frame every `intervalMs` (default 10s) but only calls onEmotion
 * when the detected emotion actually CHANGES or confidence shifts meaningfully.
 * This eliminates the glitchy re-render cascade that happened on every poll.
 */
export default function Webcam({ onEmotion, intervalMs = 10000, active = true }) {
  const videoRef   = useRef(null)
  const canvasRef  = useRef(null)
  const timerRef   = useRef(null)
  const lastRef    = useRef({ emotion: null, confidence: 0 }) // track last reported value
  const pendingRef = useRef(false)                             // prevent overlapping requests

  const [status, setStatus] = useState('starting') // starting | live | denied
  const [display, setDisplay] = useState(null)     // only for the overlay UI

  // ── Camera startup ──────────────────────────────────────────────────────────
  useEffect(() => {
    let stream
    async function start() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 480, height: 360 },
          audio: false,
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          await videoRef.current.play()
          setStatus('live')
        }
      } catch (_) {
        setStatus('denied')
      }
    }
    if (active) start()
    return () => {
      if (stream) stream.getTracks().forEach((t) => t.stop())
      clearInterval(timerRef.current)
    }
  }, [active])

  // ── Capture loop ─────────────────────────────────────────────────────────────
  useEffect(() => {
    if (status !== 'live' || !active) return

    async function capture() {
      if (pendingRef.current) return          // skip if last request still in flight
      const v = videoRef.current
      const c = canvasRef.current
      if (!v || !c || v.videoWidth === 0) return

      pendingRef.current = true
      try {
        c.width  = v.videoWidth
        c.height = v.videoHeight
        c.getContext('2d').drawImage(v, 0, 0, c.width, c.height)
        const dataUrl = c.toDataURL('image/jpeg', 0.6)   // slightly lower quality = faster

        const result = await api.analyzeEmotion(dataUrl)

        const prev = lastRef.current
        const emotionChanged    = result.emotion !== prev.emotion
        const confidenceShifted = Math.abs((result.confidence || 0) - prev.confidence) > 0.15

        // Always update the webcam overlay
        setDisplay(result)

        // Only bubble up to parent (triggering adaptive API calls) when something meaningful changed
        if (emotionChanged || confidenceShifted) {
          lastRef.current = { emotion: result.emotion, confidence: result.confidence || 0 }
          onEmotion?.(result)
        }
      } catch (_) {
        // network hiccup — silently skip
      } finally {
        pendingRef.current = false
      }
    }

    // First capture after a short delay (let video settle)
    const firstTimer = setTimeout(capture, 1500)
    timerRef.current = setInterval(capture, intervalMs)
    return () => {
      clearTimeout(firstTimer)
      clearInterval(timerRef.current)
    }
  }, [status, active, intervalMs, onEmotion])

  const meta = display ? emotionMeta(display.emotion) : null

  return (
    <div className="glass rounded-2xl overflow-hidden">
      <div className="relative bg-black/40 aspect-[4/3]">
        <video ref={videoRef} className="w-full h-full object-cover" muted playsInline />
        <canvas ref={canvasRef} className="hidden" />

        {/* Live badge */}
        {status === 'live' && (
          <div className="absolute top-3 left-3 flex items-center gap-2 text-xs font-medium px-2.5 py-1 rounded-full bg-black/50 backdrop-blur">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            LIVE
          </div>
        )}

        {/* Emotion overlay — only re-renders when display changes */}
        {meta && status === 'live' && (
          <div
            className="absolute bottom-3 left-3 right-3 flex items-center gap-3 px-3 py-2 rounded-xl bg-black/55 backdrop-blur"
            style={{ boxShadow: `0 0 22px ${meta.glow}` }}
          >
            <span className="text-2xl">{meta.emoji}</span>
            <div className="flex-1">
              <div className="text-sm font-semibold" style={{ color: meta.color }}>{meta.label}</div>
              <div className="h-1.5 mt-1 rounded-full bg-white/10 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${Math.round((display.confidence || 0) * 100)}%`,
                    background: meta.color,
                  }}
                />
              </div>
            </div>
            <span className="text-xs text-slate-300">{Math.round((display.confidence || 0) * 100)}%</span>
          </div>
        )}

        {/* Permission denied */}
        {status === 'denied' && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6 gap-3">
            <span className="text-3xl">🔒</span>
            <p className="text-sm font-semibold text-slate-200">Camera access blocked</p>
            <p className="text-xs text-slate-400 leading-relaxed max-w-[220px]">
              Click the camera icon in your browser address bar, choose <b>Allow</b>, then refresh.
            </p>
            <p className="text-[11px] text-slate-600 mt-1">Running in demo mode — emotions are simulated.</p>
          </div>
        )}

        {/* Starting */}
        {status === 'starting' && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-sm text-slate-400 animate-pulse">Starting camera…</span>
          </div>
        )}
      </div>

      <div className="px-4 py-2 text-[11px] text-slate-400 flex justify-between">
        <span>Emotion sampled every {intervalMs / 1000}s</span>
        {display && <span className="font-mono">engine: {display.engine}</span>}
      </div>
    </div>
  )
}