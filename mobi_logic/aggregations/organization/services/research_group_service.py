from mobi_logic import get_repository


def remove_research_group(user_id, unit_id, research_group_id):
    UnitRepository = get_repository('UnitRepository')

    unit = UnitRepository.get_unit(user_id, unit_id)

    unit.remove_research_group_id(research_group_id)


def remove_survey(research_group_id, survey_id):
    """Remove survey from research group id"""
    ResearchGroupRepository = get_repository('ResearchGroupRepository')

    research_group = ResearchGroupRepository.get_research_group(research_group_id)

    research_group.remove_survey(survey_id)


def remove_question(survey_id, question_id):
    """Remove question from survey"""
    SurveyRepository = get_repository('SurveyRepository')

    survey = SurveyRepository.get_survey(survey_id)

    survey.remove_question(question_id)


def remove_response(question_id, response_id):
    """Remove question from survey"""
    QuestionRepository = get_repository('QuestionRepository')

    question = QuestionRepository.get_question(question_id)

    question.remove_response(response_id)

