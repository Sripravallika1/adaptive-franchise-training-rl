"""
analysis/plots.py
-----------------
Generates learning curve plots for control vs treatment groups.
Saves plots as PNG files so you can include them in your paper
or send them to Dr. Cumberland.

Requires matplotlib: pip install matplotlib
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os


def plot_learning_curves(control_avg, treatment_avg, save_path="results/learning_curves.png"):
    """
    Plots all 5 metrics over time for control vs treatment groups.
    Saves as a PNG file.

    Args:
        control_avg:   averaged metric tracking dict for control group
        treatment_avg: averaged metric tracking dict for treatment group
        save_path:     where to save the plot
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    metrics = [
        ("attention", "Attention Consistency", "higher = better"),
        ("response_control", "Response Control", "higher = better"),
        ("learning_efficiency", "Learning Efficiency", "positive = improving"),
        ("cognitive_load", "Cognitive Load", "lower = better"),
        ("error_pattern", "Error Pattern", "lower = better"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle(
        "KFC Franchise Adaptive Training Simulation\nControl vs Treatment — Metric Trajectories",
        fontsize=14, fontweight="bold", y=1.02
    )

    axes_flat = axes.flatten()

    for idx, (key, title, note) in enumerate(metrics):
        ax = axes_flat[idx]
        rounds = control_avg["round"]

        ax.plot(rounds, control_avg[key], label="Control", color="#2196F3",
                linewidth=2, marker="o", markersize=3)
        ax.plot(rounds, treatment_avg[key], label="Treatment", color="#FF5722",
                linewidth=2, marker="s", markersize=3)

        ax.set_title(f"{title}\n({note})", fontsize=10, fontweight="bold")
        ax.set_xlabel("Training Round", fontsize=9)
        ax.set_ylabel(key.replace("_", " ").title(), fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)

    # Use last panel for profile summary placeholder
    axes_flat[5].axis("off")
    axes_flat[5].text(
        0.5, 0.5,
        "Adaptive system detects\nlearner profiles missed\nby standardized training.",
        ha="center", va="center", fontsize=11,
        style="italic", color="#555555",
        transform=axes_flat[5].transAxes
    )

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\n  Plot saved to: {save_path}")


def plot_profile_distribution(control_classified, treatment_classified,
                               save_path="results/learner_profiles.png"):
    """
    Plots learner profile distribution for control vs treatment.
    Shows how adaptive training detects different learner types.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    profiles = ["efficient", "deep_learner", "impulsive", "attention_variable", "struggling"]
    control_counts = [control_classified["counts"].get(p, 0) for p in profiles]
    treatment_counts = [treatment_classified["counts"].get(p, 0) for p in profiles]

    x = range(len(profiles))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar([i - width/2 for i in x], control_counts, width,
                   label="Control", color="#2196F3", alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], treatment_counts, width,
                   label="Treatment", color="#FF5722", alpha=0.8)

    ax.set_title("Learner Profile Distribution\nControl vs Treatment Group",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Learner Profile", fontsize=11)
    ax.set_ylabel("Number of Learners", fontsize=11)
    ax.set_xticks(list(x))
    ax.set_xticklabels([p.replace("_", "\n") for p in profiles], fontsize=9)
    ax.legend(fontsize=10)
    ax.grid(True, axis="y", alpha=0.3)

    # Add value labels on bars
    for bar in bars1:
        if bar.get_height() > 0:
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                   str(int(bar.get_height())), ha="center", va="bottom", fontsize=9)
    for bar in bars2:
        if bar.get_height() > 0:
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                   str(int(bar.get_height())), ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved to: {save_path}")
