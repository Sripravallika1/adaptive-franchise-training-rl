import numpy as np

def compute_cognitive_load_proxy(history):
    """Cognitive load from response times and error count."""
    times = [i.response_time for i in history]
    errors = [not i.correct for i in history]
    if not times:
        return 0
    return np.mean(times) + sum(errors)
