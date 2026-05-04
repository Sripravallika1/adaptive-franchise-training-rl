# Full implementation of Attention Metric
import numpy as np

def compute_attention_consistency(history):
    """Attention consistency based on response time variance."""
    times = [i.response_time for i in history]
    if len(times) < 2:
        return 0
    return 1 / (1 + np.std(times))
