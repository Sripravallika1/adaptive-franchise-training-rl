from experiments.run_simulation import run_simulation
from constants import NUM_LEARNERS, NUM_ROUNDS


if __name__ == "__main__":
    print("=" * 60)
    print("KFC FRANCHISE ADAPTIVE TRAINING SIMULATION")
    print("=" * 60)
    print(f"Running {NUM_LEARNERS} learners x {NUM_ROUNDS} rounds...")
    print("Control group: standard training (fixed easy difficulty)")
    print("Treatment group: adaptive training (policy-based adjustment)")
    print("")

    control, treatment = run_simulation(
        num_learners=NUM_LEARNERS,
        num_rounds=NUM_ROUNDS
    )

    def avg_metric(group, metric_key):
        return sum(l["final_metrics"][metric_key] for l in group) / len(group)

    print("=" * 60)
    print("RESULTS - GROUP COMPARISON")
    print("=" * 60)
    print(f"{'Metric':<20} {'Control':<15} {'Treatment':<15} {'Difference':<15}")
    print("-" * 60)

    for metric_key in ["attention", "response_control", "learning_efficiency", "cognitive_load", "error_pattern"]:
        control_avg = avg_metric(control, metric_key)
        treatment_avg = avg_metric(treatment, metric_key)
        diff = treatment_avg - control_avg
        print(f"{metric_key:<20} {control_avg:<15.3f} {treatment_avg:<15.3f} {diff:<15.3f}")

    print("=" * 60)
    print(f"Average mastery count - Control:   {sum(l['mastery_count'] for l in control) / len(control):.2f}")
    print(f"Average mastery count - Treatment: {sum(l['mastery_count'] for l in treatment) / len(treatment):.2f}")
    print("=" * 60)
