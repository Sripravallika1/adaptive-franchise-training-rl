"""
experiments/run_simulation.py
------------------------------
Runs control vs treatment simulation.
Now returns both result dicts AND raw LearnerProfile objects
so metrics_over_time and learning_profiles can use them.
"""

import random
from data_models import LearnerProfile, LearnerInteraction
from metrics import compute_all_metrics
from simulator.adaptive_policy import apply_policy, apply_knowledge_decay, check_spaced_repetition
from constants import (
    NUM_SKILLS_PER_LEARNER, SUCCESS_RATE_MULTIPLIERS,
    DECAY_CHECK_INTERVAL, NUM_LEARNERS, NUM_ROUNDS
)


def generate_mock_interaction(difficulty, question_id):
    """Generate a mock interaction based on current difficulty."""
    success_rate = SUCCESS_RATE_MULTIPLIERS[difficulty]
    correct = random.random() < success_rate
    multiplier = {"easy": 1, "medium": 2, "hard": 3}[difficulty]
    response_time = random.uniform(1, 3) * multiplier
    return LearnerInteraction(question_id, correct, response_time)


def run_simulation(num_learners=NUM_LEARNERS, num_rounds=NUM_ROUNDS):
    """
    Run control vs treatment simulation.

    Returns:
        control_results:   list of result dicts
        treatment_results: list of result dicts
        control_profiles:  list of raw LearnerProfile objects
        treatment_profiles: list of raw LearnerProfile objects
    """
    control_group = []
    treatment_group = []

    for i in range(num_learners):
        control = LearnerProfile(f"control_{i}")
        control.group = "control"
        control.difficulty = "easy"
        for s in range(NUM_SKILLS_PER_LEARNER):
            control.skills[s] = 1.0
            control.last_reviewed[s] = 0
        control_group.append(control)

        treatment = LearnerProfile(f"treatment_{i}")
        treatment.group = "treatment"
        treatment.difficulty = "easy"
        for s in range(NUM_SKILLS_PER_LEARNER):
            treatment.skills[s] = 1.0
            treatment.last_reviewed[s] = 0
        treatment_group.append(treatment)

    for round_num in range(1, num_rounds + 1):
        for learner in control_group + treatment_group:
            skill_id = random.randint(0, NUM_SKILLS_PER_LEARNER - 1)
            interaction = generate_mock_interaction(learner.difficulty, skill_id)
            learner.add_interaction(interaction)

            if interaction.correct:
                learner.consecutive_wrong = 0
            else:
                learner.consecutive_wrong += 1

            if learner.group == "treatment" and len(learner.history) >= 3:
                metrics = compute_all_metrics(learner.history)
                learner = apply_policy(learner, metrics, round_num)

            if round_num % DECAY_CHECK_INTERVAL == 0:
                apply_knowledge_decay(learner, round_num)

            check_spaced_repetition(learner, round_num)

    def finalize(group):
        results = []
        for learner in group:
            metrics = compute_all_metrics(learner.history)
            results.append({
                "learner_id": learner.learner_id,
                "group": learner.group,
                "final_metrics": metrics,
                "final_difficulty": learner.difficulty,
                "mastery_count": sum(
                    1 for s in learner.skills
                    if learner.skills[s] >= 0.80
                ),
            })
        return results

    return (
        finalize(control_group),
        finalize(treatment_group),
        control_group,
        treatment_group
    )


def get_learner_profiles(num_learners=NUM_LEARNERS, num_rounds=NUM_ROUNDS):
    """Convenience function returning only raw profiles."""
    _, _, control, treatment = run_simulation(num_learners, num_rounds)
    return control, treatment
