from mobi_logic import get_repository


def remove_research_group(user_id, unit_id, research_group_id):
    UnitRepository = get_repository('UnitRepository')

    unit = UnitRepository.get_unit(user_id, unit_id)

    unit.remove_research_group_id(research_group_id)


def remove_survey(user_id, unit_id, research_group_id, survey_id):
    """Remove survey from research group id"""
    UnitRepository = get_repository('UnitRepository')

    unit = UnitRepository.get_unit(user_id, unit_id)
    research_group = unit.get_research_group(research_group_id)

    research_group.remove_survey(survey_id)


def remove_question(user_id, unit_id, research_group_id, survey_id, question_id):
    """Remove question from survey"""
    UnitRepository = get_repository('UnitRepository')

    unit = UnitRepository.get_unit(user_id, unit_id)
    research_group = unit.get_research_group(research_group_id)
    survey = research_group.get_survey(survey_id)

    survey.remove_question(question_id)


def remove_response(user_id, unit_id, research_group_id, survey_id, question_id, response_id):
    """Remove question from survey"""
    UnitRepository = get_repository('UnitRepository')

    unit = UnitRepository.get_unit(user_id, unit_id)
    research_group = unit.get_research_group(research_group_id)
    survey = research_group.get_survey(survey_id)
    question = survey.get_question(question_id)

    question.remove_response(response_id)


def get_research_group_license(research_group_code):
    ResearchGroupRepository = get_repository('ResearchGroupRepository')
    rs = ResearchGroupRepository.get_by_code(research_group_code)
    return rs.license


