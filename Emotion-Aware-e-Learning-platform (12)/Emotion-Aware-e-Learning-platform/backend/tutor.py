"""
tutor.py
========
The platform's signature feature set:

1. CHATBOT  -> tutor_reply(): an emotion-aware conversational tutor that answers
   student questions, explains concepts and motivates. It works fully offline
   with a rich rule + retrieval engine, and will transparently upgrade to the
   Anthropic API if an ANTHROPIC_API_KEY is present in the environment.

2. IMMEDIATE RESPONSE SYSTEM -> instant_intervention(): the moment an emotion is
   detected the backend can fire a short, targeted intervention (a nudge, a
   breather, a confidence line) without the student having to ask. This is what
   makes the session feel alive and reactive.
"""

import os
import re
import random

from courses import COURSES

# ---------------------------------------------------------------------------
# Knowledge snippets the offline tutor can retrieve from, keyed by topic words.
# ---------------------------------------------------------------------------
_KNOWLEDGE = {
    "variable": "A variable is a name that points to a value. In Python you just assign (x = 5); in Java you declare a type first (int x = 5;).",
    "loop": "Loops repeat work. Use a 'for' loop when you know how many times (or to walk a collection) and a 'while' loop when you repeat until a condition changes.",
    "function": "A function is reusable, named logic. It takes inputs (parameters), does work, and usually returns a result. Small functions that do one thing are easiest to test.",
    "list": "A list (Python) or ArrayList (Java) is an ordered, growable collection. Index from 0, and remember that lists are mutable.",
    "dictionary": "A dictionary maps keys to values with very fast lookup. In Java the equivalent is HashMap. Reach for it whenever you'd otherwise search a list by name.",
    "recursion": "Recursion is when a function calls itself on a smaller input. Always define a base case that stops the recursion, or it runs forever.",
    "class": "A class is a blueprint; an object is an instance of it. Fields hold state, methods define behaviour, and the constructor sets up a new object.",
    "string": "Strings are sequences of characters. They're immutable in both Python and Java, so 'editing' one actually makes a new string.",
    "array": "An array is a fixed-size, indexed block of one type. Java arrays use arr.length; going past the end throws an out-of-bounds error.",
    "exception": "An exception signals something went wrong at runtime. Wrap risky code in try/except (Python) or try/catch (Java) to handle it gracefully.",
    "prime": "A prime number has exactly two divisors: 1 and itself. To test n, try dividing by every number from 2 up to the square root of n.",
    "fibonacci": "The Fibonacci sequence starts 0, 1 and each next number is the sum of the previous two. It's a classic way to practise loops and recursion.",
}

# Emotion-flavoured opening lines for the chatbot.
_EMOTION_TONE = {
    "happy":    ["Love the energy! ", "You're clearly in the zone. ", "Great momentum - "],
    "sad":      ["No rush at all. ", "Let's take this gently. ", "We'll go one small step at a time. "],
    "angry":    ["Totally fair to feel stuck. ", "Let's slow right down. ", "Deep breath - we'll untangle this. "],
    "fear":     ["You're safe to get this wrong here. ", "We'll do it together. ", "Nothing scary about this - "],
    "surprise": ["Good catch! ", "Interesting, right? ", "Let's explore that. "],
    "neutral":  ["", "Sure thing. ", "Here you go. "],
}

# Short, instant interventions fired by the emotion detector.
_INTERVENTIONS = {
    "happy": [
        "You're flying through this - want to try the bonus challenge?",
        "Strong focus detected. I've queued up a harder question when you're ready.",
    ],
    "sad": [
        "Looks like this stretch is heavy. I've simplified the next explanation for you.",
        "Hey, progress isn't always linear. Let's make the next step an easy win.",
    ],
    "angry": [
        "Sensing some frustration - I've slowed the pace and swapped in a gentler example.",
        "Let's reset for a second. This concept trips up almost everyone at first.",
    ],
    "fear": [
        "A little uncertainty is normal here. I'll walk you through the next one step by step.",
        "You don't have to get this perfectly. Let's solve one example together.",
    ],
    "surprise": [
        "Something caught your attention - here's an interactive twist on it.",
        "That reaction is a great sign of curiosity. Want to dig deeper?",
    ],
    "neutral": [
        "Cruising along nicely. Keep going!",
        "Steady focus - you're right on track.",
    ],
}


def instant_intervention(emotion, confidence=1.0):
    """
    The IMMEDIATE RESPONSE SYSTEM. Given a freshly detected emotion, return a
    short proactive message (or None when nothing needs saying). Designed to be
    called every few seconds from the emotion loop.
    """
    emotion = (emotion or "neutral").lower()
    if confidence < 0.3:
        return None  # don't react to noisy, low-confidence reads
    # Neutral fires only occasionally so we don't spam encouragement.
    if emotion == "neutral" and random.random() > 0.25:
        return None
    pool = _INTERVENTIONS.get(emotion, _INTERVENTIONS["neutral"])
    return {
        "emotion": emotion,
        "message": random.choice(pool),
        "urgent": emotion in ("angry", "fear", "sad"),
    }


def _retrieve(message):
    """Find the most relevant knowledge snippet for a free-text question."""
    msg = message.lower()
    best = None
    for key, text in _KNOWLEDGE.items():
        if re.search(rf"\b{re.escape(key)}", msg):
            best = text
            break
    return best


def _offline_reply(message, emotion, course_id, module_title):
    """Rule + retrieval tutor used when no LLM key is configured."""
    tone = random.choice(_EMOTION_TONE.get(emotion, _EMOTION_TONE["neutral"]))
    msg = message.lower().strip()

    # Intent: greeting
    if re.match(r"^(hi|hey|hello|yo|sup)\b", msg):
        return tone + "I'm your AI tutor. Ask me anything about the lesson, or say 'explain' and a topic."

    # Intent: motivation / stuck
    if any(w in msg for w in ["stuck", "hard", "confus", "don't get", "dont get", "give up", "difficult"]):
        course_name = COURSES.get(course_id, {}).get("name", "this")
        return (tone + f"That's a normal part of learning {course_name}. Let's shrink the problem: "
                "tell me the exact line or idea that isn't clicking and we'll take just that piece.")

    # Intent: ask for an explanation -> retrieve
    snippet = _retrieve(message)
    if snippet:
        followup = {
            "happy": " Want a harder example to test it?",
            "sad": " Want me to break it down even smaller?",
            "angry": " We can go slower if you like.",
            "fear": " I can walk through an example with you next.",
            "surprise": " There's a neat edge case too if you're curious.",
            "neutral": " Ask if you'd like an example.",
        }.get(emotion, "")
        return tone + snippet + followup

    # Fallback: contextual nudge tied to the current module
    where = f" We're on '{module_title}'." if module_title else ""
    return (tone + "Good question." + where +
            " Try rephrasing with a keyword like 'loop', 'function', 'class' or 'recursion' "
            "and I'll explain it for your current course.")


def _llm_reply(message, emotion, course_id, module_title, history):
    """Optional upgrade path: call the Anthropic API if a key is configured."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        course_name = COURSES.get(course_id, {}).get("name", "programming")
        system = (
            f"You are a warm, concise programming tutor for a {course_name} course. "
            f"The student's current lesson is '{module_title}'. Their detected emotion is "
            f"'{emotion}'. Adapt: if sad/angry/fear, simplify and reassure; if happy/surprise, "
            f"stretch them. Keep replies under 90 words and end with one small next step."
        )
        msgs = []
        for turn in (history or [])[-6:]:
            role = "assistant" if turn.get("role") == "tutor" else "user"
            msgs.append({"role": role, "content": turn.get("text", "")})
        msgs.append({"role": "user", "content": message})
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=system,
            messages=msgs,
        )
        return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    except Exception:
        return None


def tutor_reply(message, emotion="neutral", course_id="python", module_title="", history=None):
    """
    Main chatbot entry point. Tries the LLM if configured, otherwise uses the
    offline engine. Always returns a dict the frontend can render.
    """
    emotion = (emotion or "neutral").lower()
    text = None
    engine = "offline"
    if os.environ.get("ANTHROPIC_API_KEY"):
        text = _llm_reply(message, emotion, course_id, module_title, history)
        engine = "anthropic" if text else "offline"
    if not text:
        text = _offline_reply(message, emotion, course_id, module_title)
    return {"role": "tutor", "text": text, "emotion": emotion, "engine": engine}
