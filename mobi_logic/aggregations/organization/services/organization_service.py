from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.question import Question
from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup
from mobi_logic.aggregations.organization.domain.entities.response import Response
from mobi_logic.aggregations.organization.domain.entities.survey import Survey
from mobi_logic.aggregations.organization.domain.entities.unit import Unit


class OrganizationService:

    @staticmethod
    def get_units(user_id):
        UnitRepository = get_repository('UnitRepository')
        units = UnitRepository.get_all_units(user_id)
        filtered_units = []

        for unit in units:
            filtered_research_group = []
            for rs in unit.research_groups:
                if rs.status != ResearchGroup.STATUS.DELETED:
                    filtered_research_group.append(rs)
            unit.research_groups = filtered_research_group
            filtered_units.append(unit)

        return filtered_units

    @staticmethod
    def get_research_group(user_id, unit_id, research_group_id):
        UnitRepository = get_repository('UnitRepository')
        unit = UnitRepository.get_unit(user_id, unit_id)
        return unit.get_research_group(research_group_id)

    @staticmethod
    def get_surveys(user_id, unit_id, research_group_id):
        UnitRepository = get_repository('UnitRepository')
        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        filtered_surveys = []
        for survey in rs.surveys:
            if survey.status != Survey.STATUS.DELETED:
                filtered_surveys.append(survey)

        return filtered_surveys

    @staticmethod
    def get_questions(user_id, unit_id, research_group_id, survey_id):
        UnitRepository = get_repository('UnitRepository')
        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)
        survey = rs.get_survey(survey_id)

        filtered_questions = []

        for question in survey.questions:
            if question.status != Question.STATUS.DELETED:
                filtered_questions.append(question)

        return filtered_questions

    @staticmethod
    def get_responses(user_id, unit_id, research_group_id, survey_id, question_id):
        UnitRepository = get_repository('UnitRepository')
        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)
        survey = rs.get_survey(survey_id)
        question = survey.get_question(question_id)
        filtered_responses = []

        for response in question.responses:
            if response.status != Response.STATUS.DELETED:
                filtered_responses.append(response)

        return filtered_responses

    @staticmethod
    def update_research_group(user_id, unit_id, research_group_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        rs.update_values(data)

    @staticmethod
    def update_survey(user_id, unit_id, research_group_id, survey_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        survey = rs.get_survey(survey_id)

        survey.update_values(data)

        SurveyTimeRepository = get_repository('SurveyTimeRepository')
        if 'time' in data:
            SurveyTimeRepository.delete_all(survey_id)

        if data.get('time'):
            SurveyTimeRepository = get_repository('SurveyTimeRepository')
            SurveyTimeRepository.delete_all(survey_id)
            for survey_time in data.get('time'):
                OrganizationService.create_survey_time(user_id, unit_id, research_group_id, survey_id, survey_time)

    @staticmethod
    def update_question(user_id, unit_id, research_group_id, survey_id, question_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        survey = rs.get_survey(survey_id)
        question = survey.get_question(question_id)

        question.update_values(data)

    @staticmethod
    def update_response(user_id, unit_id, research_group_id, survey_id, question_id, response_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        survey = rs.get_survey(survey_id)
        question = survey.get_question(question_id)
        response = question.get_response(response_id)

        response.update_values(data)


    @staticmethod
    def create_unit(user_id, data):
        UnitRepository = get_repository('UnitRepository')
        unit = Unit()
        unit.configure(user_id=user_id,
                       name=data['name'],
                       description=data['description'])

        UnitRepository.save(unit)
        return unit

    @staticmethod
    def create_research_group(user_id, unit_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)

        unit.create_research_group(data['name'],
                                   code=data.get('code'),
                                   description=data.get('description'))

        return unit

    @staticmethod
    def create_survey(user_id, unit_id, research_group_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)

        rs = unit.get_research_group(research_group_id)
        rs.create_survey(data['name'], description=data.get('description'), )

        return unit

    @staticmethod
    def create_question(user_id, unit_id, research_group_id, survey_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)

        rs = unit.get_research_group(research_group_id)
        survey = rs.get_survey(survey_id)
        survey.create_question(data['name'], data['type'])

        return unit

    @staticmethod
    def create_response(user_id, unit_id, research_group_id, survey_id, question_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)

        rs = unit.get_research_group(research_group_id)
        survey = rs.get_survey(survey_id)
        question = survey.get_question(question_id)
        response_id = question.create_response(data['value'], data['type'])

        return response_id

    @staticmethod
    def create_survey_time(user_id, unit_id, research_group_id, survey_id, survey_time):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        survey = rs.get_survey(survey_id)

        survey.add_time(survey_time)
