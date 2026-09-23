"""
database.py
===========
Progress + analytics storage. Uses MongoDB when MONGO_URI is reachable,
otherwise falls back to a thread-safe in-memory store so the app runs
anywhere with zero setup.

Stores per-user:
  - completed_modules
  - quiz_scores
  - emotion_log
  - challenge_completions
"""

import os
import time
import threading
from collections import defaultdict

_MONGO_OK = False
_collection = None

try:
    from pymongo import MongoClient
    uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    _client = MongoClient(uri, serverSelectionTimeoutMS=800)
    _client.server_info()  # forces a connection check
    _collection = _client["emotion_elearning"]["progress"]
    _MONGO_OK = True
except Exception:
    _MONGO_OK = False


class _MemoryStore:
    """Minimal in-memory stand-in for the Mongo collection we use."""
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def _doc(self, user):
        if user not in self._data:
            self._data[user] = {
                "user": user,
                "completed_modules": [],
                "quiz_scores": [],
                "emotion_log": [],
                "challenge_completions": [],
                "created": time.time(),
            }
        return self._data[user]

    def record_module(self, user, module_id):
        with self._lock:
            d = self._doc(user)
            if module_id not in d["completed_modules"]:
                d["completed_modules"].append(module_id)

    def record_quiz(self, user, payload):
        with self._lock:
            self._doc(user)["quiz_scores"].append({**payload, "ts": time.time()})

    def record_emotion(self, user, emotion, confidence):
        with self._lock:
            log = self._doc(user)["emotion_log"]
            log.append({"emotion": emotion, "confidence": confidence, "ts": time.time()})
            del log[:-500]  # cap history

    def record_challenge(self, user, challenge_title, passed):
        with self._lock:
            self._doc(user)["challenge_completions"].append(
                {"challenge": challenge_title, "passed": passed, "ts": time.time()}
            )

    def get(self, user):
        with self._lock:
            return dict(self._doc(user))


_mem = _MemoryStore()


# --- Mongo-backed helpers (mirror the memory store API) --------------------
def _mongo_get(user):
    doc = _collection.find_one({"user": user})
    if not doc:
        doc = {"user": user, "completed_modules": [], "quiz_scores": [],
               "emotion_log": [], "challenge_completions": [], "created": time.time()}
        _collection.insert_one(doc)
    doc.pop("_id", None)
    return doc


def record_module(user, module_id):
    if _MONGO_OK:
        _collection.update_one({"user": user}, {"$addToSet": {"completed_modules": module_id}}, upsert=True)
    else:
        _mem.record_module(user, module_id)


def record_quiz(user, payload):
    entry = {**payload, "ts": time.time()}
    if _MONGO_OK:
        _collection.update_one({"user": user}, {"$push": {"quiz_scores": entry}}, upsert=True)
    else:
        _mem.record_quiz(user, payload)


def record_emotion(user, emotion, confidence):
    if _MONGO_OK:
        _collection.update_one(
            {"user": user},
            {"$push": {"emotion_log": {"$each": [{"emotion": emotion, "confidence": confidence, "ts": time.time()}],
                                       "$slice": -500}}},
            upsert=True,
        )
    else:
        _mem.record_emotion(user, emotion, confidence)


def record_challenge(user, challenge_title, passed):
    if _MONGO_OK:
        _collection.update_one(
            {"user": user},
            {"$push": {"challenge_completions": {"challenge": challenge_title, "passed": passed, "ts": time.time()}}},
            upsert=True,
        )
    else:
        _mem.record_challenge(user, challenge_title, passed)


def get_progress(user):
    doc = _mongo_get(user) if _MONGO_OK else _mem.get(user)
    return _with_analytics(doc)


def _with_analytics(doc):
    """Derive simple learning analytics from the raw record."""
    quizzes = doc.get("quiz_scores", [])
    emotions = doc.get("emotion_log", [])
    challenges = doc.get("challenge_completions", [])

    avg_quiz = round(sum(q.get("score_pct", 0) for q in quizzes) / len(quizzes), 1) if quizzes else 0
    emo_counts = defaultdict(int)
    for e in emotions:
        emo_counts[e.get("emotion", "neutral")] += 1
    dominant = max(emo_counts, key=emo_counts.get) if emo_counts else "neutral"
    passed_challenges = sum(1 for c in challenges if c.get("passed"))

    return {
        "user": doc.get("user"),
        "completed_modules": doc.get("completed_modules", []),
        "quiz_scores": quizzes,
        "emotion_log": emotions[-50:],
        "challenge_completions": challenges,
        "analytics": {
            "modules_completed": len(doc.get("completed_modules", [])),
            "quizzes_taken": len(quizzes),
            "average_quiz_score": avg_quiz,
            "challenges_passed": passed_challenges,
            "emotion_distribution": dict(emo_counts),
            "dominant_emotion": dominant,
            "storage": "mongodb" if _MONGO_OK else "in-memory",
        },
    }


def db_status():
    return {"mongodb": _MONGO_OK, "mode": "mongodb" if _MONGO_OK else "in-memory"}
