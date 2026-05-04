class LearnerInteraction:
    """Single learner response to a training question."""
    def __init__(self, question_id, correct, response_time):
        self.question_id = question_id
        self.correct = correct
        self.response_time = response_time


class LearnerProfile:
    """Learner state across all training rounds."""
    def __init__(self, learner_id):
        self.learner_id = learner_id
        self.history = []
        self.difficulty = "easy"
        self.skills = {}
        self.mastery = {}
        self.last_reviewed = {}
        self.consecutive_wrong = 0
        self.group = None

    def add_interaction(self, interaction):
        """Add interaction to history."""
        self.history.append(interaction)
