class QuestionRepository:
    def __init__(self):
        self._questions = {}

    def get_question(self, question_id):
        if question_id in self._questions:
            return self._questions[question_id]

    def save(self, question):
        self._questions[question.id] = question
