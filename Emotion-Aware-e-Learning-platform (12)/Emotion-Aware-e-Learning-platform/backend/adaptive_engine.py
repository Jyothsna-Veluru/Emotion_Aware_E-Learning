"""
adaptive_engine.py
==================
The heart of the platform: turn a detected emotion into concrete adaptations
of pace, difficulty, examples and quiz selection.

Returned 'directive' is consumed by the frontend to actually change what the
student sees, and by quiz_engine to pick the right difficulty tier.
"""

# Emotion -> adaptation policy.
POLICY = {
    "happy": {
        "quiz_difficulty": "hard",
        "pace": "accelerate",
        "example": "advanced",
        "show_bonus": True,
        "headline": "You're on a roll - let's push further.",
        "actions": ["Unlock the bonus challenge", "Switch to advanced examples", "Harder quiz questions"],
        "accent": "#22c55e",
    },
    "sad": {
        "quiz_difficulty": "easy",
        "pace": "slow",
        "example": "basic",
        "show_bonus": False,
        "headline": "Let's break this into smaller, friendlier steps.",
        "actions": ["Simplified explanation", "Easier quiz", "Encouragement from your tutor"],
        "accent": "#60a5fa",
    },
    "angry": {
        "quiz_difficulty": "easy",
        "pace": "slow",
        "example": "basic",
        "show_bonus": False,
        "headline": "Taking the pressure off - one calm step at a time.",
        "actions": ["Slower pace", "Gentler examples", "A short reset before the quiz"],
        "accent": "#f87171",
    },
    "fear": {
        "quiz_difficulty": "easy",
        "pace": "guided",
        "example": "basic",
        "show_bonus": False,
        "headline": "You've got this - we'll solve one together first.",
        "actions": ["Fully guided worked example", "Confidence-building quiz", "Step-by-step hints"],
        "accent": "#a78bfa",
    },
    "surprise": {
        "quiz_difficulty": "medium",
        "pace": "interactive",
        "example": "advanced",
        "show_bonus": True,
        "headline": "Curiosity sparked - here's something interactive.",
        "actions": ["Interactive challenge", "A surprising edge case", "Medium quiz"],
        "accent": "#fbbf24",
    },
    "neutral": {
        "quiz_difficulty": "medium",
        "pace": "steady",
        "example": "basic",
        "show_bonus": False,
        "headline": "Steady progress - continuing as planned.",
        "actions": ["Continue the lesson", "Standard examples", "Medium quiz"],
        "accent": "#94a3b8",
    },
}


def adapt(emotion, confidence=1.0):
    """Return a full adaptation directive for the given emotion."""
    emotion = (emotion or "neutral").lower()
    base = POLICY.get(emotion, POLICY["neutral"])
    # Low-confidence detections soften toward 'neutral' to avoid whiplash.
    if confidence < 0.35 and emotion != "neutral":
        directive = dict(POLICY["neutral"])
        directive["headline"] = "Reading the room - keeping things steady for now."
        directive["source_emotion"] = emotion
        directive["low_confidence"] = True
        return directive
    directive = dict(base)
    directive["source_emotion"] = emotion
    directive["low_confidence"] = False
    return directive


def pick_example(module, emotion, confidence=1.0):
    """Choose basic vs advanced example text based on emotion."""
    directive = adapt(emotion, confidence)
    key = directive["example"]
    examples = module.get("examples", {})
    return examples.get(key) or examples.get("basic", "")
