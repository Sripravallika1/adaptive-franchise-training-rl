"""
analysis/metrics_over_time.py
------------------------------
Tracks all 5 behavioral metrics across every round of training.
Produces a learning curve showing how each metric evolves over time.
This is the data you need to plot learning trajectories in your paper.
"""

from metrics import compute_all_metrics


def track_metrics_over_time(learner, window=5):
    """
    Computes metrics at each round using a sliding window of interactions.

    Args:
        learner: LearnerProfile with full interaction history
        window:  number of recent interactions to use per round (default 5)

    Returns:
        dict of lists — one value per round for each metric
        e.g. {"attention": [0.6, 0.7, ...], "cognitive_load": [...], ...}
    """
    history = learner.history
    if len(history) < window:
        return None

    tracking = {
        "round": [],
        "attention": [],
        "response_control": [],
        "learning_efficiency": [],
        "cognitive_load": [],
        "error_pattern": [],
    }

    for i in range(window, len(history) + 1):
        window_slice = history[max(0, i - window):i]
        m = compute_all_metrics(window_slice)
        tracking["round"].append(i)
        tracking["attention"].append(m["attention"])
        tracking["response_control"].append(m["response_control"])
        tracking["learning_efficiency"].append(m["learning_efficiency"])
        tracking["cognitive_load"].append(m["cognitive_load"])
        tracking["error_pattern"].append(m["error_pattern"])

    return tracking


def average_tracking_across_group(group_profiles, window=5):
    """
    Averages metric trajectories across all learners in a group.
    Produces one smooth learning curve per metric for the whole group.

    Args:
        group_profiles: list of LearnerProfile objects
        window: sliding window size

    Returns:
        dict of averaged metric lists across all learners
    """
    all_tracking = [track_metrics_over_time(l, window) for l in group_profiles]
    all_tracking = [t for t in all_tracking if t is not None]

    if not all_tracking:
        return None

    num_rounds = min(len(t["round"]) for t in all_tracking)
    averaged = {key: [] for key in ["attention", "response_control",
                                     "learning_efficiency", "cognitive_load",
                                     "error_pattern"]}

    for i in range(num_rounds):
        for metric in averaged:
            avg = sum(t[metric][i] for t in all_tracking) / len(all_tracking)
            averaged[metric].append(round(avg, 4))

    averaged["round"] = list(range(window, window + num_rounds))
    return averaged


def print_learning_curves(control_avg, treatment_avg):
    """
    Prints a round-by-round comparison of control vs treatment groups.
    Shows how each metric evolves over training rounds.
    """
    metrics = ["attention", "response_control", "learning_efficiency",
               "cognitive_load", "error_pattern"]

    print("\n" + "=" * 70)
    print("LEARNING CURVES — CONTROL VS TREATMENT (per round)")
    print("=" * 70)

    for metric in metrics:
        print(f"\n  {metric.upper()}")
        print(f"  {'Round':<8} {'Control':<12} {'Treatment':<12} {'Diff':<10}")
        print(f"  {'-'*40}")

        rounds = control_avg["round"]
        for i, r in enumerate(rounds):
            if i >= len(treatment_avg[metric]):
                break
            c = control_avg[metric][i]
            t = treatment_avg[metric][i]
            diff = t - c
            marker = " <" if metric == "learning_efficiency" and diff > 0 else ""
            print(f"  {r:<8} {c:<12.4f} {t:<12.4f} {diff:<10.4f}{marker}")
