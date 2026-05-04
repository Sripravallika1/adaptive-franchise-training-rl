"""
cognition/reward_function.py
-----------------------------
Formalizes what "good" looks like for the adaptive system.
This is the reward signal that connects the prototype to a full RL model.

In a real RL system, the agent learns to maximize cumulative reward.
Here we define the reward explicitly so it can be tracked and validated.

Reward components:
  + accuracy gain       (learning is improving)
  + cognitive load drop (learner is less overloaded)
  - cognitive load rise (learner is more overloaded)
  - error increase      (more mistakes after action)
"""


def compute_reward(metrics_before, metrics_after):
    """
    Computes reward signal based on change in learner state.

    Args:
        metrics_before: dict of metrics before policy action
        metrics_after:  dict of metrics after policy action

    Returns:
        float reward value (positive = good outcome, negative = bad)
    """
    reward = 0.0

    # Learning efficiency gain is the primary reward signal
    efficiency_delta = (metrics_after["learning_efficiency"] -
                        metrics_before["learning_efficiency"])
    reward += efficiency_delta * 2.0  # weighted heavily

    # Cognitive load reduction is rewarded
    load_delta = (metrics_before["cognitive_load"] -
                  metrics_after["cognitive_load"])
    reward += load_delta * 0.5  # weighted moderately

    # Attention improvement is rewarded
    attention_delta = (metrics_after["attention"] -
                       metrics_before["attention"])
    reward += attention_delta * 1.0

    # Error pattern increase is penalized
    error_delta = (metrics_after["error_pattern"] -
                   metrics_before["error_pattern"])
    reward -= error_delta * 1.5  # penalized

    return round(reward, 4)


def compute_cumulative_reward(reward_history):
    """
    Returns total cumulative reward across all training rounds.
    Higher = better overall training trajectory.
    """
    return round(sum(reward_history), 4)


def classify_reward(reward):
    """
    Classifies a reward value into a human-readable category.
    Useful for logging and paper reporting.
    """
    if reward > 0.2:
        return "strong positive"
    elif reward > 0.05:
        return "mild positive"
    elif reward > -0.05:
        return "neutral"
    elif reward > -0.2:
        return "mild negative"
    else:
        return "strong negative"
