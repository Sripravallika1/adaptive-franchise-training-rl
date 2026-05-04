"""
main.py
-------
Entry point for the KFC Franchise Adaptive Training Simulation.
Now includes:
  1. Metrics over time (learning curves)
  2. Reward function tracking
  3. Learner profile classification
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.run_simulation import run_simulation, get_learner_profiles
from constants import NUM_LEARNERS, NUM_ROUNDS
from analysis.metrics_over_time import average_tracking_across_group, print_learning_curves
from analysis.learning_profiles import classify_group, print_profile_summary


def avg_metric(group, metric_key):
    """Compute average of a metric across a group."""
    return sum(l["final_metrics"][metric_key] for l in group) / len(group)


if __name__ == "__main__":
    print("=" * 70)
    print("  KFC FRANCHISE ADAPTIVE TRAINING SIMULATION")
    print("=" * 70)
    print(f"  Running {NUM_LEARNERS} learners x {NUM_ROUNDS} rounds...")
    print("  Control:   standard training (fixed easy difficulty)")
    print("  Treatment: adaptive training (policy-based adjustment)")
    print("")

    control_results, treatment_results, control_profiles, treatment_profiles = run_simulation(
        num_learners=NUM_LEARNERS,
        num_rounds=NUM_ROUNDS
    )

    # --- SECTION 1: Final Results ---
    print("=" * 70)
    print("  RESULTS — FINAL GROUP COMPARISON")
    print("=" * 70)
    print(f"  {'Metric':<22} {'Control':<14} {'Treatment':<14} {'Difference':<12}")
    print(f"  {'-' * 60}")

    for key in ["attention", "response_control", "learning_efficiency",
                "cognitive_load", "error_pattern"]:
        c = avg_metric(control_results, key)
        t = avg_metric(treatment_results, key)
        diff = t - c
        print(f"  {key:<22} {c:<14.3f} {t:<14.3f} {diff:<12.3f}")

    print("=" * 70)
    print(f"  Avg mastery — Control:   {sum(l['mastery_count'] for l in control_results) / len(control_results):.2f}")
    print(f"  Avg mastery — Treatment: {sum(l['mastery_count'] for l in treatment_results) / len(treatment_results):.2f}")

    # --- SECTION 2: Learning Curves ---
    control_avg = average_tracking_across_group(control_profiles)
    treatment_avg = average_tracking_across_group(treatment_profiles)
    if control_avg and treatment_avg:
        print_learning_curves(control_avg, treatment_avg)

    # --- SECTION 3: Learner Profiles ---
    control_classified = classify_group(control_profiles)
    treatment_classified = classify_group(treatment_profiles)
    print_profile_summary(control_classified, treatment_classified)
