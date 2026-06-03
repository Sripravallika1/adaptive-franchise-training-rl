import numpy as np


def cohens_d(group1, group2):
    """Computes Cohen's d effect size between two groups."""
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = np.mean(group1), np.mean(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return round((mean2 - mean1) / pooled_std, 4)


def interpret_d(d):
    """Returns interpretation of Cohen's d."""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "negligible"
    elif abs_d < 0.5:
        return "small"
    elif abs_d < 0.8:
        return "medium"
    else:
        return "large"


def compute_effect_sizes(control_results, treatment_results):
    """Computes Cohen's d for all five metrics between groups."""
    metric_keys = ["attention", "response_control", "learning_efficiency",
                   "cognitive_load", "error_pattern"]
    effect_sizes = {}
    for key in metric_keys:
        c = [r["final_metrics"][key] for r in control_results]
        t = [r["final_metrics"][key] for r in treatment_results]
        d = cohens_d(c, t)
        effect_sizes[key] = {
            "cohens_d": d,
            "interpretation": interpret_d(d),
            "direction": "treatment > control" if d > 0 else "control > treatment"
        }
    return effect_sizes


def print_effect_sizes(effect_sizes):
    """Prints effect sizes in a clean table."""
    print("\n" + "=" * 70)
    print("  EFFECT SIZES (Cohen's d) — Control vs Treatment")
    print("=" * 70)
    print(f"  {'Metric':<22} {'d':<10} {'Magnitude':<12} {'Direction'}")
    print(f"  {'-' * 64}")
    for key, vals in effect_sizes.items():
        print(f"  {key:<22} {vals['cohens_d']:<10.4f} {vals['interpretation']:<12} {vals['direction']}")
    print("=" * 70)
    print("  Reference: small=0.2, medium=0.5, large=0.8")
