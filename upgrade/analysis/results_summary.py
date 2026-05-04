"""
analysis/results_summary.py
-----------------------------
Runs multiple simulation trials and aggregates results.
Produces stable, reproducible statistics for your paper.

Instead of one run (which varies due to randomness), this runs
the simulation N times and averages the results — giving you
more robust numbers to report.
"""

import numpy as np
from experiments.run_simulation import run_simulation


def run_aggregated_experiment(num_runs=10, num_learners=50, num_rounds=20):
    """
    Runs the simulation multiple times and aggregates results.

    Args:
        num_runs:    number of independent simulation runs
        num_learners: learners per run
        num_rounds:  rounds per run

    Returns:
        dict with mean, std, and difference for each metric
    """
    print(f"\n  Running {num_runs} simulation trials...")

    metric_keys = ["attention", "response_control", "learning_efficiency",
                   "cognitive_load", "error_pattern"]

    control_scores = {k: [] for k in metric_keys}
    treatment_scores = {k: [] for k in metric_keys}

    for run in range(1, num_runs + 1):
        print(f"  Trial {run}/{num_runs}...", end="\r")
        control, treatment, _, _ = run_simulation(num_learners, num_rounds)

        for k in metric_keys:
            c_avg = sum(l["final_metrics"][k] for l in control) / len(control)
            t_avg = sum(l["final_metrics"][k] for l in treatment) / len(treatment)
            control_scores[k].append(c_avg)
            treatment_scores[k].append(t_avg)

    print(f"  {num_runs} trials complete.              ")

    results = {}
    for k in metric_keys:
        c_mean = np.mean(control_scores[k])
        t_mean = np.mean(treatment_scores[k])
        c_std = np.std(control_scores[k])
        t_std = np.std(treatment_scores[k])
        results[k] = {
            "control_mean": round(c_mean, 4),
            "control_std": round(c_std, 4),
            "treatment_mean": round(t_mean, 4),
            "treatment_std": round(t_std, 4),
            "difference": round(t_mean - c_mean, 4),
        }

    return results


def print_aggregated_results(results, num_runs):
    """Prints aggregated results in a clean table format."""
    print("\n" + "=" * 75)
    print(f"  AGGREGATED RESULTS ({num_runs} simulation trials)")
    print("=" * 75)
    print(f"  {'Metric':<22} {'Control':<18} {'Treatment':<18} {'Difference':<12}")
    print(f"  {'':22} {'Mean (SD)':<18} {'Mean (SD)':<18}")
    print(f"  {'-' * 68}")

    for key, vals in results.items():
        c = f"{vals['control_mean']:.3f} ({vals['control_std']:.3f})"
        t = f"{vals['treatment_mean']:.3f} ({vals['treatment_std']:.3f})"
        d = vals['difference']
        direction = "↑" if key == "learning_efficiency" and d > 0 else ""
        print(f"  {key:<22} {c:<18} {t:<18} {d:<+.4f} {direction}")

    print("=" * 75)
    print(f"\n  Note: Values reported as Mean (SD) across {num_runs} independent trials.")
    print(f"  Positive difference = Treatment > Control.")
