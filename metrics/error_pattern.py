from collections import Counter

def compute_error_pattern(history):
    """Detect proportion of repeated errors on same question."""
    errors = [i.question_id for i in history if not i.correct]
    if not errors:
        return 0
    counts = Counter(errors)
    repeated_errors = sum(1 for c in counts.values() if c > 1)
    return repeated_errors / len(errors)
