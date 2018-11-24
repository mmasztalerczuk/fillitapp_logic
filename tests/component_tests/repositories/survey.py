class SurveyRepository:
    def __init__(self):
        self._surveys = {}

    def get_survey(self, survey_id):
        if survey_id in self._surveys:
            return self._surveys[survey_id]

    def save(self, survey):
        self._surveys[survey.id] = survey
