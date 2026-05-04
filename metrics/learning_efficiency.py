def compute_learning_efficiency(history):
    """Improvement score: second half accuracy minus first half accuracy."""
    if len(history) < 2:
        return 0
    mid = len(history) // 2
    first_half = history[:mid]
    second_half = history[mid:]
    acc1 = sum(i.correct for i in first_half) / len(first_half)
    acc2 = sum(i.correct for i in second_half) / len(second_half)
    return acc2 - acc1
