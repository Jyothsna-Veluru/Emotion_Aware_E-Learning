"""
app.py
======
Emotion-Aware e-Learning Platform - Flask backend.

Run:
    pip install -r requirements.txt
    python app.py
Server starts on http://localhost:5000

Endpoints
---------
GET  /health                       -> service + engine status
GET  /courses                      -> course catalog
GET  /course/<course_id>           -> full course (no answers)
POST /analyze-emotion              -> emotion from a base64 webcam frame
POST /adaptive-response            -> adaptation directive for an emotion
POST /intervention                 -> IMMEDIATE proactive nudge for an emotion
POST /tutor-chat                   -> AI tutor chatbot reply
POST /quiz                         -> emotion-adapted quiz for a module
POST /submit-quiz                  -> grade a quiz submission
POST /submit-challenge             -> record a coding-challenge result
POST /complete-module              -> mark a module complete
GET  /progress?user=<id>           -> progress + analytics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

import emotion_engine
import adaptive_engine
import quiz_engine
import tutor
import database
from courses import list_courses, get_course

app = Flask(__name__)
CORS(app, origins="*")


@app.get("/")
def root():
    """Confirms the backend is alive when accessed directly via IP."""
    return jsonify({
        "service": "Emotion-Aware e-Learning Platform backend",
        "status": "ok",
        "hint": "Use /health for full status, /courses for content.",
    })

def _user():
    """Resolve the user id from query or JSON body; default to 'demo'."""
    if request.method == "GET":
        return request.args.get("user", "demo")
    data = request.get_json(silent=True) or {}
    return data.get("user", "demo")


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Emotion-Aware e-Learning Platform",
        "emotion_engine": emotion_engine.engine_status(),
        "database": database.db_status(),
        "tutor_llm": bool(__import__("os").environ.get("ANTHROPIC_API_KEY")),
    })


@app.get("/courses")
def courses():
    return jsonify({"courses": list_courses()})


@app.get("/course/<course_id>")
def course(course_id):
    data = get_course(course_id, include_answers=False)
    if not data:
        return jsonify({"error": "course not found"}), 404
    return jsonify(data)


@app.post("/analyze-emotion")
def analyze_emotion():
    data = request.get_json(silent=True) or {}
    image = data.get("image")
    result = emotion_engine.analyze_frame(image)
    # log the read for analytics
    database.record_emotion(_user(), result["emotion"], result["confidence"])
    return jsonify(result)


@app.post("/adaptive-response")
def adaptive_response():
    data = request.get_json(silent=True) or {}
    emotion = data.get("emotion", "neutral")
    confidence = float(data.get("confidence", 1.0))
    directive = adaptive_engine.adapt(emotion, confidence)
    return jsonify(directive)


@app.post("/intervention")
def intervention():
    """IMMEDIATE RESPONSE SYSTEM endpoint."""
    data = request.get_json(silent=True) or {}
    emotion = data.get("emotion", "neutral")
    confidence = float(data.get("confidence", 1.0))
    result = tutor.instant_intervention(emotion, confidence)
    return jsonify({"intervention": result})


@app.post("/tutor-chat")
def tutor_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "message required"}), 400
    reply = tutor.tutor_reply(
        message=message,
        emotion=data.get("emotion", "neutral"),
        course_id=data.get("course_id", "python"),
        module_title=data.get("module_title", ""),
        history=data.get("history", []),
    )
    return jsonify(reply)


@app.post("/quiz")
def quiz():
    data = request.get_json(silent=True) or {}
    built = quiz_engine.build_quiz(
        course_id=data.get("course_id", "python"),
        module_id=data.get("module_id", ""),
        emotion=data.get("emotion", "neutral"),
        confidence=float(data.get("confidence", 1.0)),
    )
    if not built:
        return jsonify({"error": "course or module not found"}), 404
    built.pop("_key", None)  # never leak the answer key
    return jsonify(built)


@app.post("/submit-quiz")
def submit_quiz():
    data = request.get_json(silent=True) or {}
    result = quiz_engine.grade(
        course_id=data.get("course_id", "python"),
        module_id=data.get("module_id", ""),
        answers=data.get("answers", {}),
        emotion=data.get("emotion", "neutral"),
        confidence=float(data.get("confidence", 1.0)),
    )
    if not result:
        return jsonify({"error": "course or module not found"}), 404
    database.record_quiz(_user(), {
        "course_id": result["course_id"],
        "module_id": result["module_id"],
        "score_pct": result["score_pct"],
    })
    return jsonify(result)


@app.post("/submit-challenge")
def submit_challenge():
    data = request.get_json(silent=True) or {}
    title = data.get("challenge_title", "Coding Challenge")
    passed = bool(data.get("passed", False))
    database.record_challenge(_user(), title, passed)
    return jsonify({"recorded": True, "challenge_title": title, "passed": passed})


@app.post("/complete-module")
def complete_module():
    data = request.get_json(silent=True) or {}
    module_id = data.get("module_id")
    if not module_id:
        return jsonify({"error": "module_id required"}), 400
    database.record_module(_user(), module_id)
    return jsonify({"recorded": True, "module_id": module_id})


@app.get("/progress")
def progress():
    return jsonify(database.get_progress(_user()))


if __name__ == "__main__":
    import socket
    try:
        lan_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        lan_ip = "<your-LAN-ip>"
    status = emotion_engine.engine_status()
    print("=" * 60)
    print(" Emotion-Aware e-Learning Platform - backend")
    print(f"   emotion engine : {status['mode']}")
    print(f"   database       : {database.db_status()['mode']}")
    print(f"   local          : http://localhost:5000")
    print(f"   network        : http://{lan_ip}:5000")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)