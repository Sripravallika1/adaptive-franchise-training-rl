"""
analysis/learning_profiles.py
------------------------------
Classifies each learner into a behavioral profile based on their metrics.
This is the "wow factor" piece — shows the adaptive system responding
differently to different learner types.

Four profiles (based on cognitive psychology literature):
  - Efficient:           fast + accurate + low load
  - Deep Learner:        slow + accurate + improving
  - Impulsive:           fast + inaccurate + high error pattern
  - Attention Variable:  inconsistent attention + variable performance
"""

from metrics import compute_all_metrics


PROFILES = {
    "efficient": "Fast, accurate, low cognitive load. Ready for challenge.",
    "deep_learner": "Slower but steady. Improving over time. Needs patience.",
    "impulsive": "Fast but inaccurate. Needs slowing down and more feedback.",
    "attention_variable": "Inconsistent attention. Needs shorter chunks and structure.",
    "struggling": "High load, low accuracy, not improving. Needs simplification.",
}


def classify_learner(learner):
    """
    Classifies a learner into one of five behavioral profiles.

    Args:
        learner: LearnerProfile with interaction history

    Returns:
        tuple: (profile_name, description, metrics_dict)
    """
    if len(learner.history) < 5:
        return ("insufficient_data", "Not enough interactions to classify.", {})

    metrics = compute_all_metrics(learner.history)

    attention = metrics["attention"]
    response_control = metrics["response_control"]
    learning_efficiency = metrics["learning_efficiency"]
    cognitive_load = metrics["cognitive_load"]
    error_pattern = metrics["error_pattern"]

    # Efficient: high attention, high control, positive efficiency, low load
    if (attention > 0.6 and response_control > 0.3 and
            learning_efficiency > 0.05 and cognitive_load < 6.0):
        profile = "efficient"

    # Impulsive: low response control, high error pattern
    elif response_control < 0.15 and error_pattern > 0.3:
        profile = "impulsive"

    # Struggling: high load, negative efficiency
    elif cognitive_load > 10.0 and learning_efficiency < -0.1:
        profile = "struggling"

    # Attention Variable: low attention consistency
    elif attention < 0.35:
        profile = "attention_variable"

    # Deep Learner: improving despite slower pace
    elif learning_efficiency > 0.0:
        profile = "deep_learner"

    # Default
    else:
        profile = "attention_variable"

    return (profile, PROFILES[profile], metrics)


def classify_group(learner_profiles):
    """
    Classifies all learners in a group and returns a summary.

    Args:
        learner_profiles: list of LearnerProfile objects

    Returns:
        dict with profile counts and per-learner classifications
    """
    counts = {p: 0 for p in PROFILES}
    classifications = []

    for learner in learner_profiles:
        profile, description, metrics = classify_learner(learner)
        if profile in counts:
            counts[profile] += 1
        classifications.append({
            "learner_id": learner.learner_id,
            "profile": profile,
            "description": description,
            "final_difficulty": learner.difficulty,
        })

    return {"counts": counts, "learners": classifications}


def print_profile_summary(control_profiles, treatment_profiles):
    """
    Prints a side-by-side comparison of learner profile distributions
    between control and treatment groups.
    """
    print("\n" + "=" * 70)
    print("LEARNER PROFILE DISTRIBUTION")
    print("=" * 70)
    print(f"  {'Profile':<22} {'Control':<12} {'Treatment':<12}")
    print(f"  {'-' * 44}")

    for profile in PROFILES:
        c = control_profiles["counts"].get(profile, 0)
        t = treatment_profiles["counts"].get(profile, 0)
        print(f"  {profile:<22} {c:<12} {t:<12}")

    print(f"\n  Total learners: {sum(control_profiles['counts'].values())} per group")
