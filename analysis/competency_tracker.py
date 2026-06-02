"""
analysis/competency_tracker.py
Tracks how many rounds each learner takes to reach mastery threshold.
Measures H4: adaptive trainees reach competency in fewer rounds.
"""

import numpy as np
from constants import MASTERY_ACCURACY, MASTERY_MIN_ATTEMPTS


def rounds_to_competency(learner):
    """Returns the round when learner first achieved mastery, or None."""
    history = learner.history
    if len(history) < MASTERY_MIN_ATTEMPTS:
        return None
    for i in range(MASTERY_MIN_ATTEMPTS, len(history) + 1):
        window = history[i - MASTERY_MIN_ATTEMPTS:i]
        accuracy = sum(x.correct for x in window) / len(window)
        if accuracy >= MASTERY_ACCURACY:
            return i
    return None


def compute_group_competency(learner_profiles):
    """Computes time to competency stats for a group."""
    times = []
    never_mastered = 0
    for learner in learner_profiles:
        t = rounds_to_competency(learner)
        if t is not None:
            times.append(t)
        else:
            never_mastered += 1
    total = len(learner_profiles)
    if not times:
        return {"mean_rounds": None, "median_rounds": None,
                "pct_mastered": 0.0, "never_mastered": never_mastered}
    return {
        "mean_rounds": round(float(np.mean(times)), 2),
        "median_rounds": round(float(np.median(times)), 2),
        "pct_mastered": round(len(times) / total * 100, 1),
        "never_mastered": never_mastered
    }


def print_competency_comparison(control_stats, treatment_stats):
    """Prints time to competency comparison between groups."""
    print("\n" + "=" * 70)
    print("  TIME TO COMPETENCY (H4)")
    print("=" * 70)
    print(f"  {'Metric':<30} {'Control':<18} {'Treatment'}")
    print(f"  {'-' * 60}")
    c = control_stats
    t = treatment_stats
    print(f"  {'Mean rounds to mastery':<30} {str(c['mean_rounds']):<18} {t['mean_rounds']}")
    print(f"  {'Median rounds to mastery':<30} {str(c['median_rounds']):<18} {t['median_rounds']}")
    print(f"  {'% who reached mastery':<30} {str(c['pct_mastered'])+'%':<18} {str(t['pct_mastered'])+'%'}")
    print(f"  {'Never mastered':<30} {str(c['never_mastered']):<18} {t['never_mastered']}")
    print("=" * 70)
