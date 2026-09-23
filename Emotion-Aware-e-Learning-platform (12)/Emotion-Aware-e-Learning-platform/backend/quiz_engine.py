"""
quiz_engine.py
==============
Selects quiz questions by difficulty (driven by the adaptive engine) and
grades submissions. Answers live only in courses.py with include_answers=True
so the client never receives the key.
"""

from courses import get_course
from adaptive_engine import adapt

_DIFFICULTY_ORDER = ["easy", "medium", "hard"]


def build_quiz(course_id, module_id, emotion="neutral", confidence=1.0, limit=5):
    """
    Return up to `limit` questions for a module, ordered so the tier matching
    the student's emotion comes first, then the rest. Answers are stripped.
    """
    course = get_course(course_id, include_answers=True)
    if not course:
        return None
    module = next((m for m in course["modules"] if m["id"] == module_id), None)
    if not module:
        return None

    target = adapt(emotion, confidence)["quiz_difficulty"]

    def sort_key(q):
        d = q.get("difficulty", "medium")
        primary = 0 if d == target else 1
        return (primary, _DIFFICULTY_ORDER.index(d))

    ordered = sorted(module["quiz"], key=sort_key)[:limit]
    # Store each question's original index so grade() can look up the right
    # answer even after reordering. orig_idx is stripped before sending to
    # the client (same as _key) — it lives only in the internal _key map.
    orig_indices = [module["quiz"].index(q) for q in ordered]
    public = [
        {"id": i, "q": q["q"], "options": q["options"], "difficulty": q.get("difficulty", "medium")}
        for i, q in enumerate(ordered)
    ]
    # _key maps display-position -> (orig_index, correct_answer)
    key = {i: {"orig_idx": orig_indices[i], "answer": module["quiz"][orig_indices[i]]["answer"]}
           for i in range(len(ordered))}
    return {
        "course_id": course_id,
        "module_id": module_id,
        "adapted_to": emotion,
        "target_difficulty": target,
        "questions": public,
        "_key": key,                       # internal, stripped before sending
    }


def grade(course_id, module_id, answers, emotion="neutral", confidence=1.0):
    """
    Grade a submission. `answers` is {display_position: chosen_option_index}.
    We rebuild the same sorted question order that build_quiz() used so that
    display-position 0 maps to the correct original quiz entry, regardless of
    how the adaptive engine reordered questions by difficulty.
    """
    course = get_course(course_id, include_answers=True)
    if not course:
        return None
    module = next((m for m in course["modules"] if m["id"] == module_id), None)
    if not module:
        return None

    quiz = module["quiz"]

    # Rebuild the same ordering build_quiz() used so positions align.
    target = adapt(emotion, confidence)["quiz_difficulty"]

    def sort_key(q):
        d = q.get("difficulty", "medium")
        primary = 0 if d == target else 1
        return (primary, _DIFFICULTY_ORDER.index(d))

    ordered = sorted(quiz, key=sort_key)[:len(answers)]
    # Map display-position -> original quiz entry
    position_to_orig = {i: quiz.index(q) for i, q in enumerate(ordered)}

    total = 0
    correct = 0
    breakdown = []
    for idx_str, chosen in answers.items():
        try:
            pos = int(idx_str)
        except (TypeError, ValueError):
            continue
        if pos not in position_to_orig:
            continue
        orig_idx = position_to_orig[pos]
        total += 1
        right = quiz[orig_idx]["answer"]
        is_correct = int(chosen) == right
        correct += int(is_correct)
        breakdown.append({
            "index": pos,
            "question": quiz[orig_idx]["q"],
            "your_answer": chosen,
            "correct_answer": right,
            "correct": is_correct,
            "difficulty": quiz[orig_idx].get("difficulty", "medium"),
        })

    pct = round(100 * correct / total) if total else 0
    return {
        "course_id": course_id,
        "module_id": module_id,
        "correct": correct,
        "total": total,
        "score_pct": pct,
        "passed": pct >= 60,
        "breakdown": breakdown,
    }