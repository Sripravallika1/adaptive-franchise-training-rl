from constants import (
    IMPULSIVE_RT_THRESHOLD, IMPULSIVE_ACCURACY_THRESHOLD,
    OVERLOAD_RT_THRESHOLD, OVERLOAD_ACCURACY_THRESHOLD,
    STUCK_WRONG_IN_A_ROW, MASTERY_ACCURACY, MASTERY_MIN_ATTEMPTS,
    DECAY_RATE_PER_DAY, REVIEW_TRIGGER_THRESHOLD, REVIEW_INTERVALS_DAYS,
    KNOWLEDGE_REVIEW_INCREASE
)


def apply_policy(learner, metrics, current_round):
    """Apply adaptive policy rules in order — first match wins."""
    if not learner.history:
        return learner

    avg_rt = sum(i.response_time for i in learner.history) / len(learner.history)
    accuracy = sum(i.correct for i in learner.history) / len(learner.history)

    # Rule 1: IMPULSIVE — fast but inaccurate
    if avg_rt < IMPULSIVE_RT_THRESHOLD and accuracy < IMPULSIVE_ACCURACY_THRESHOLD:
        learner.difficulty = "easy"
        return learner

    # Rule 2: OVERLOAD — slow and inaccurate
    if avg_rt > OVERLOAD_RT_THRESHOLD and accuracy < OVERLOAD_ACCURACY_THRESHOLD:
        learner.difficulty = "easy"
        return learner

    # Rule 3: STUCK — repeated wrong answers
    if learner.consecutive_wrong >= STUCK_WRONG_IN_A_ROW:
        return learner

    # Rule 4: READY TO ADVANCE — improving and low load
    if metrics["learning_efficiency"] > 0.15 and metrics["cognitive_load"] < 5.0:
        order = ["easy", "medium", "hard"]
        idx = order.index(learner.difficulty)
        if idx < 2:
            learner.difficulty = order[idx + 1]
        return learner

    # Rule 5: DEFAULT — on track
    return learner


def check_mastery(learner, skill_id):
    """Return True if learner has mastered a skill."""
    skill_history = [i for i in learner.history if i.question_id == skill_id]
    if len(skill_history) < MASTERY_MIN_ATTEMPTS:
        return False
    accuracy = sum(i.correct for i in skill_history) / len(skill_history)
    return accuracy >= MASTERY_ACCURACY


def apply_knowledge_decay(learner, current_round):
    """Apply exponential knowledge decay to all skills."""
    for skill_id in learner.skills:
        last = learner.last_reviewed.get(skill_id, current_round)
        days = current_round - last
        learner.skills[skill_id] *= (1 - DECAY_RATE_PER_DAY) ** days
        if learner.skills[skill_id] < REVIEW_TRIGGER_THRESHOLD:
            learner.skills[skill_id] = REVIEW_TRIGGER_THRESHOLD


def check_spaced_repetition(learner, current_round):
    """Trigger review for skills at scheduled intervals."""
    for skill_id in learner.skills:
        last = learner.last_reviewed.get(skill_id, 0)
        days_since = current_round - last
        if days_since in REVIEW_INTERVALS_DAYS:
            learner.skills[skill_id] = min(1.0, learner.skills[skill_id] + KNOWLEDGE_REVIEW_INCREASE)
            learner.last_reviewed[skill_id] = current_round# Adaptive Policy Engine with rule-based decision logic

# Your code here...
