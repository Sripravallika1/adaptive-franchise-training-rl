"""
main.py
-------
Entry point for the KFC Franchise Adaptive Training Simulation.

Runs:
  1. Single simulation with full output
  2. Learning curve plots (saved to results/)
  3. Learner profile distribution plot (saved to results/)
  4. Aggregated results across 10 trials
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.run_simulation import run_simulation
from constants import NUM_LEARNERS, NUM_ROUNDS
from analysis.metrics_over_time import average_tracking_across_group, print_learning_curves
from analysis.learning_profiles import classify_group, print_profile_summary
from analysis.plots import plot_learning_curves, plot_profile_distribution
from analysis.results_summary import run_aggregated_experiment, print_aggregated_results


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

    # --- Single simulation run ---
    control_results, treatment_results, control_profiles, treatment_profiles = run_simulation(
        num_learners=NUM_LEARNERS,
        num_rounds=NUM_ROUNDS
    )

    # --- Section 1: Final comparison ---
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
        print(f"  {key:<22} {c:<14.3f} {t:<14.3f} {diff:<+.3f}")

    print("=" * 70)
    print(f"  Avg mastery — Control:   {sum(l['mastery_count'] for l in control_results) / len(control_results):.2f}")
    print(f"  Avg mastery — Treatment: {sum(l['mastery_count'] for l in treatment_results) / len(treatment_results):.2f}")

    # --- Section 2: Learning curves ---
    control_avg = average_tracking_across_group(control_profiles)
    treatment_avg = average_tracking_across_group(treatment_profiles)
    if control_avg and treatment_avg:
        print_learning_curves(control_avg, treatment_avg)

    # --- Section 3: Learner profiles ---
    control_classified = classify_group(control_profiles)
    treatment_classified = classify_group(treatment_profiles)
    print_profile_summary(control_classified, treatment_classified)

    # --- Section 4: Save plots ---
    print("\n  Generating plots...")
    if control_avg and treatment_avg:
        plot_learning_curves(control_avg, treatment_avg)
        plot_profile_distribution(control_classified, treatment_classified)

    # --- Section 5: Aggregated results (10 trials) ---
    print("\n  Running aggregated experiment (10 trials for robust stats)...")
    agg_results = run_aggregated_experiment(num_runs=10,
                                             num_learners=NUM_LEARNERS,
                                             num_rounds=NUM_ROUNDS)
    print_aggregated_results(agg_results, num_runs=10)

    print("\n  Done. Check results/ folder for plots.")
