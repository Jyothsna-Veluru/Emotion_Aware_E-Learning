"""
emotion_engine.py
=================
Wraps DeepFace + OpenCV for facial-emotion recognition.

Design goal: the backend must START and RESPOND even if the heavy ML stack
(DeepFace / TensorFlow / OpenCV) is not installed. So we try to import them
lazily. If they are present, we run real inference on a base64 webcam frame.
If they are absent, we fall back to a lightweight deterministic heuristic so
the whole platform stays demoable on any machine.

Public API:
    analyze_frame(image_b64) -> dict(emotion, confidence, scores, engine)
    engine_status()          -> dict describing which backend is active
"""

import base64
import io
import time
import random

# Canonical label set the rest of the app understands.
EMOTIONS = ["happy", "sad", "angry", "fear", "surprise", "neutral"]

# DeepFace returns "disgust" too; we fold it into "angry" for our 6-label model.
_DEEPFACE_MAP = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "disgust": "angry",
    "fear": "fear",
    "surprise": "surprise",
    "neutral": "neutral",
}

_DEEPFACE_OK = False
_CV2_OK = False
_np = None

try:
    import numpy as _np  # noqa
    _NP_OK = True
except Exception:
    _NP_OK = False

try:
    import cv2  # noqa
    _CV2_OK = True
except Exception:
    _CV2_OK = False

try:
    from deepface import DeepFace  # noqa
    _DEEPFACE_OK = True
except Exception:
    DeepFace = None
    _DEEPFACE_OK = False


def engine_status():
    return {
        "deepface": _DEEPFACE_OK,
        "opencv": _CV2_OK,
        "numpy": _NP_OK,
        "mode": "deepface" if _DEEPFACE_OK else "heuristic-fallback",
    }


def _decode_b64_image(image_b64):
    """Turn a data URL or raw base64 string into an OpenCV BGR ndarray."""
    if not image_b64:
        return None
    if "," in image_b64:           # strip 'data:image/jpeg;base64,' prefix
        image_b64 = image_b64.split(",", 1)[1]
    try:
        raw = base64.b64decode(image_b64)
    except Exception:
        return None
    if not (_CV2_OK and _NP_OK):
        return raw  # return bytes; heuristic only needs a stable hash
    arr = _np.frombuffer(raw, dtype=_np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def _real_inference(img):
    """Run DeepFace emotion analysis on a decoded frame."""
    result = DeepFace.analyze(
        img,
        actions=["emotion"],
        enforce_detection=False,   # don't crash if no clear face
        detector_backend="opencv",
        silent=True,
    )
    if isinstance(result, list):
        result = result[0]
    raw_scores = result.get("emotion", {})

    # Fold into our 6-label model and normalise.
    folded = {e: 0.0 for e in EMOTIONS}
    for k, v in raw_scores.items():
        label = _DEEPFACE_MAP.get(k.lower())
        if label:
            folded[label] += float(v)
    total = sum(folded.values()) or 1.0
    scores = {k: round(v / total, 4) for k, v in folded.items()}
    top = max(scores, key=scores.get)
    return {
        "emotion": top,
        "confidence": round(scores[top], 4),
        "scores": scores,
        "engine": "deepface",
        "ts": time.time(),
    }


def _heuristic_inference(payload):
    """
    Deterministic-ish fallback. We derive a pseudo-emotion from the byte
    signature of the frame so repeated identical frames are stable, while
    a changing webcam produces natural variation. Confidence is reported
    honestly as low so the UI can flag "demo mode".
    """
    seed = sum(payload[:512]) if payload else int(time.time())
    rng = random.Random(seed)
    # Weight toward neutral/happy to feel like a calm study session.
    weights = {"neutral": 4, "happy": 3, "surprise": 2, "sad": 2, "fear": 1, "angry": 1}
    bag = []
    for e, w in weights.items():
        bag += [e] * w
    top = rng.choice(bag)
    scores = {e: round(rng.uniform(0.02, 0.15), 4) for e in EMOTIONS}
    scores[top] = round(rng.uniform(0.45, 0.7), 4)
    norm = sum(scores.values())
    scores = {k: round(v / norm, 4) for k, v in scores.items()}
    return {
        "emotion": top,
        "confidence": scores[top],
        "scores": scores,
        "engine": "heuristic-fallback",
        "ts": time.time(),
    }


def analyze_frame(image_b64):
    """Main entry point used by the /analyze-emotion route."""
    decoded = _decode_b64_image(image_b64)
    if _DEEPFACE_OK and _CV2_OK and decoded is not None and not isinstance(decoded, bytes):
        try:
            return _real_inference(decoded)
        except Exception as exc:           # any inference error -> graceful demo
            res = _heuristic_inference(decoded if isinstance(decoded, bytes) else b"")
            res["engine"] = "heuristic-fallback (deepface error)"
            res["error"] = str(exc)[:160]
            return res
    payload = decoded if isinstance(decoded, bytes) else b""
    return _heuristic_inference(payload)
