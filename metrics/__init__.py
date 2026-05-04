from .attention import compute_attention_consistency
from .response_control import compute_response_control
from .learning_efficiency import compute_learning_efficiency
from .cognitive_load import compute_cognitive_load_proxy
from .error_pattern import compute_error_pattern


def compute_all_metrics(history):
    """Compute all 5 behavioral metrics from interaction history."""
    return {
        "attention": compute_attention_consistency(history),
        "response_control": compute_response_control(history),
        "learning_efficiency": compute_learning_efficiency(history),
        "cognitive_load": compute_cognitive_load_proxy(history),
        "error_pattern": compute_error_pattern(history),
    }
