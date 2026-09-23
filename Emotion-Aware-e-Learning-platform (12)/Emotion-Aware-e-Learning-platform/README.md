# Emotion-Aware e-Learning Platform

An AI-powered educational platform that **detects student emotions through the webcam** and
**adapts learning content, quizzes, examples and tutoring in real time**.

> AI · Computer Vision · Adaptive Learning · Intelligent Tutoring · Emotion Recognition

---

## ✨ What it does

1. The webcam samples the student's face every few seconds.
2. **DeepFace + OpenCV** classify the emotion (happy, sad, angry, fear, surprise, neutral).
3. The **adaptive engine** changes pace, example difficulty and quiz difficulty to match.
4. An **AI tutor chatbot** explains concepts and motivates, adapting its tone to the emotion.
5. An **immediate-response system** fires a proactive nudge the moment frustration, anxiety
   or sadness is detected — no need for the student to ask.
6. Coding challenges, quizzes and a progress dashboard track the whole journey.

### Unique features added
- **🤖 AI Tutor Chatbot** (`/tutor-chat`) — context- and emotion-aware. Works fully offline
  with a rule + retrieval engine, and auto-upgrades to the Anthropic API if `ANTHROPIC_API_KEY`
  is set.
- **⚡ Immediate Response System** (`/intervention`) — instant, proactive interventions keyed to
  the live emotion stream.

---

## 🧱 Tech stack

| Layer     | Tech                                            |
|-----------|-------------------------------------------------|
| Frontend  | React 18, Vite, Tailwind CSS, React Router, Axios |
| Backend   | Flask, Flask-CORS                               |
| AI / CV   | DeepFace, OpenCV (pretrained — no runtime training) |
| Database  | MongoDB (auto-falls back to in-memory)          |
| Dataset   | FER2013 (research / future training — see `backend/data/`) |

> **Runs anywhere:** if DeepFace/OpenCV or MongoDB aren't installed, the backend automatically
> falls back to a heuristic emotion engine and an in-memory store, so the whole platform still
> works for a demo. Install the optional packages for the full experience.

---

## 🚀 Quick start

### 1. Backend
```bash
cd backend
pip install -r requirements.txt        # Flask + Flask-CORS are the only hard requirements
python app.py                          # http://localhost:5000
```

Optional, for real webcam emotion detection:
```bash
pip install deepface opencv-python tf-keras
```
Optional, to power the tutor with the Anthropic API:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev                            # http://localhost:5173
```
The Vite dev server proxies `/api/*` to the Flask backend automatically.

Open **http://localhost:5173**, allow camera access, pick a course, and start learning.

---

## 🔌 API reference

| Method | Endpoint              | Purpose                                   |
|--------|-----------------------|-------------------------------------------|
| GET    | `/health`             | Service + engine + DB status              |
| GET    | `/courses`            | Course catalog                            |
| GET    | `/course/<id>`        | Full course (answers stripped)            |
| POST   | `/analyze-emotion`    | Emotion from a base64 webcam frame        |
| POST   | `/adaptive-response`  | Adaptation directive for an emotion       |
| POST   | `/intervention`       | ⚡ Immediate proactive nudge               |
| POST   | `/tutor-chat`         | 🤖 AI tutor chatbot reply                  |
| POST   | `/quiz`               | Emotion-adapted quiz for a module         |
| POST   | `/submit-quiz`        | Grade a quiz submission                   |
| POST   | `/submit-challenge`   | Record a coding-challenge result          |
| POST   | `/complete-module`    | Mark a module complete                    |
| GET    | `/progress?user=<id>` | Progress + learning analytics             |

---

## 🗂️ Project structure
```
emotion-aware-elearning/
├── backend/
│   ├── app.py                # Flask app + all routes
│   ├── emotion_engine.py     # DeepFace/OpenCV + heuristic fallback
│   ├── adaptive_engine.py    # emotion -> adaptation policy
│   ├── tutor.py              # chatbot + immediate-response system
│   ├── quiz_engine.py        # adaptive quiz selection + grading
│   ├── courses.py            # full Python & Java course content
│   ├── database.py           # MongoDB + in-memory fallback
│   ├── requirements.txt
│   └── data/FER2013_README.md
├── frontend/
│   ├── src/
│   │   ├── pages/            # Landing, CourseSelect, LearningSession, QuizPage, Dashboard
│   │   ├── components/       # Webcam, TutorChat, Quiz, Challenge, NavBar
│   │   ├── api.js  emotions.js  App.jsx  main.jsx  index.css
│   ├── package.json  vite.config.js  tailwind.config.js
└── README.md
```

---

## 🎯 Emotion → adaptation map

| Emotion   | Pace        | Examples | Quiz   | Tutor behavior              |
|-----------|-------------|----------|--------|-----------------------------|
| Happy     | accelerate  | advanced | hard   | challenge & stretch         |
| Sad       | slow        | basic    | easy   | simplify & encourage        |
| Angry     | slow        | basic    | easy   | calm & reset                |
| Fear      | guided      | basic    | easy   | confidence-building, hints  |
| Surprise  | interactive | advanced | medium | explore curiosity           |
| Neutral   | steady      | basic    | medium | continue normally           |

Low-confidence detections soften toward *neutral* to avoid jarring changes.
