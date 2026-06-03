"""
main.py
Entry point for the Franchise Adaptive Training Simulation.
Includes: seed control, Cohen's d, profile curves, time to competency.
"""

import sys
import os
import random
import numpy as np

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from experiments.run_simulation import run_simulation
from constants import NUM_LEARNERS, NUM_ROUNDS
from analysis.metrics_over_time import average_tracking_across_group, print_learning_curves
from analysis.learning_profiles import classify_group, print_profile_summary
from analysis.plots import plot_learning_curves, plot_profile_distribution
from analysis.results_summary import run_aggregated_experiment, print_aggregated_results
from analysis.statistics import compute_effect_sizes, print_effect_sizes
from analysis.competency_tracker import compute_group_competency, print_competency_comparison
from analysis.profile_plots import plot_all_profile_metrics


def avg_metric(group, metric_key):
    return sum(l["final_metrics"][metric_key] for l in group) / len(group)


if __name__ == "__main__":
    print("=" * 70)
    print("  KFC FRANCHISE ADAPTIVE TRAINING SIMULATION")
    print(f"  Seed: {RANDOM_SEED} | Learners: {NUM_LEARNERS} | Rounds: {NUM_ROUNDS}")
    print("=" * 70)
    print("  Control:   standard training (fixed easy difficulty)")
    print("  Treatment: adaptive training (policy-based adjustment)")
    print("")

    control_results, treatment_results, control_profiles, treatment_profiles = run_simulation(
        num_learners=NUM_LEARNERS,
        num_rounds=NUM_ROUNDS
    )

    print("=" * 70)
    print("  RESULTS — FINAL GROUP COMPARISON")
    print("=" * 70)
    print(f"  {'Metric':<22} {'Control':<14} {'Treatment':<14} {'Difference':<12}")
    print(f"  {'-' * 60}")
    for key in ["attention", "response_control", "learning_efficiency",
                "cognitive_load", "error_pattern"]:
        c = avg_metric(control_results, key)
        t = avg_metric(treatment_results, key)
        print(f"  {key:<22} {c:<14.3f} {t:<14.3f} {t - c:<+.3f}")

    print("=" * 70)
    print(f"  Avg mastery — Control:   {sum(l['mastery_count'] for l in control_results) / len(control_results):.2f}")
    print(f"  Avg mastery — Treatment: {sum(l['mastery_count'] for l in treatment_results) / len(treatment_results):.2f}")

    effect_sizes = compute_effect_sizes(control_results, treatment_results)
    print_effect_sizes(effect_sizes)

    control_competency = compute_group_competency(control_profiles)
    treatment_competency = compute_group_competency(treatment_profiles)
    print_competency_comparison(control_competency, treatment_competency)

    control_avg = average_tracking_across_group(control_profiles)
    treatment_avg = average_tracking_across_group(treatment_profiles)
    if control_avg and treatment_avg:
        print_learning_curves(control_avg, treatment_avg)

    control_classified = classify_group(control_profiles)
    treatment_classified = classify_group(treatment_profiles)
    print_profile_summary(control_classified, treatment_classified)

    print("\n  Generating plots...")
    if control_avg and treatment_avg:
        plot_learning_curves(control_avg, treatment_avg)
        plot_profile_distribution(control_classified, treatment_classified)

    plot_all_profile_metrics(treatment_profiles)

    print("\n  Running aggregated experiment (10 trials)...")
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    agg_results = run_aggregated_experiment(
        num_runs=10,
        num_learners=NUM_LEARNERS,
        num_rounds=NUM_ROUNDS
    )
    print_aggregated_results(agg_results, num_runs=10)

    print(f"\n  Done. Seed={RANDOM_SEED}. Check results/ folder for plots.")
