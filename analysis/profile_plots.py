"""
analysis/profile_plots.py
Plots learning curves split by learner profile type.
Supports RQ4: adaptive system detects and responds to distinct learner types.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from analysis.learning_profiles import classify_learner
from analysis.metrics_over_time import track_metrics_over_time


def group_by_profile(learner_profiles):
    """Groups learners by their behavioral profile."""
    grouped = {}
    for learner in learner_profiles:
        profile, _, _ = classify_learner(learner)
        if profile not in grouped:
            grouped[profile] = []
        grouped[profile].append(learner)
    return grouped


def average_metric_for_group(learners, metric_key, window=5):
    """Averages a metric over time across a group of learners."""
    all_tracks = []
    for learner in learners:
        t = track_metrics_over_time(learner, window)
        if t and metric_key in t:
            all_tracks.append(t[metric_key])
    if not all_tracks:
        return [], []
    min_len = min(len(t) for t in all_tracks)
    avg = [np.mean([t[i] for t in all_tracks]) for i in range(min_len)]
    rounds = list(range(window, window + min_len))
    return rounds, avg


def plot_all_profile_metrics(treatment_profiles,
                              save_path="results/profile_all_metrics.png"):
    """Plots all 5 metrics split by learner profile. Core RQ4 visualization."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    grouped = group_by_profile(treatment_profiles)
    metrics = ["attention", "response_control", "learning_efficiency",
               "cognitive_load", "error_pattern"]
    colors = {
        "efficient": "#16A34A",
        "deep_learner": "#1D4ED8",
        "impulsive": "#DC2626",
        "attention_variable": "#B45309",
        "struggling": "#7C3AED"
    }
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(
        "Metric Trajectories by Learner Profile — Treatment Group\n"
        "Supporting RQ4: Adaptive system detects distinct learner types",
        fontsize=13, fontweight="bold"
    )
    axes_flat = axes.flatten()
    for idx, metric_key in enumerate(metrics):
        ax = axes_flat[idx]
        for profile, learners in grouped.items():
            if len(learners) < 2:
                continue
            rounds, avg = average_metric_for_group(learners, metric_key)
            if not rounds:
                continue
            color = colors.get(profile, "#555")
            label = f"{profile.replace('_', ' ').title()} (n={len(learners)})"
            ax.plot(rounds, avg, label=label, color=color,
                    linewidth=1.8, marker="o", markersize=2.5)
        ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
        ax.set_title(metric_key.replace("_", " ").title(),
                     fontsize=10, fontweight="bold")
        ax.set_xlabel("Round", fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7)
    axes_flat[5].axis("off")
    axes_flat[5].text(
        0.5, 0.5,
        "Each line = a distinct learner type.\n\n"
        "Standardized training treats all\nlearners identically.\n\n"
        "The adaptive system detects and\nresponds to each type.",
        ha="center", va="center", fontsize=10,
        style="italic", color="#444",
        transform=axes_flat[5].transAxes
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Profile plot saved to: {save_path}")
