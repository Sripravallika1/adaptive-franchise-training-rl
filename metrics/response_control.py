def compute_response_control(history):
    """Speed-accuracy balance: faster and more accurate = higher score."""
    if not history:
        return 0
    accuracy = sum(i.correct for i in history) / len(history)
    avg_time = sum(i.response_time for i in history) / len(history)
    return accuracy / (avg_time + 1e-5)
