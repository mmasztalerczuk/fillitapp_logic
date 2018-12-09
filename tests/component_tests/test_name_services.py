from mobi_logic import configure
from mobi_logic.aggregations.organization.domain.entities.question import Question
from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup
from mobi_logic.aggregations.organization.domain.entities.response import Response
from mobi_logic.aggregations.organization.domain.entities.survey import Survey
from mobi_logic.aggregations.organization.domain.entities.unit import Unit
from mobi_logic.aggregations.organization.services.research_group_service import remove_research_group, remove_survey, \
    remove_question, remove_response
from tests.component_tests.repositories.question import QuestionRepository
from tests.component_tests.repositories.research_group import ResearchGroupRepository
from tests.component_tests.repositories.response import ReponseRepository
from tests.component_tests.repositories.survey import SurveyRepository
from tests.component_tests.repositories.unit import UnitRepository


def test_remove_research_group():
    unit_repository = UnitRepository()
    repository = {'UnitRepository': unit_repository,
                  'ResearchGroupRepository': ResearchGroupRepository()}
    configure(repository)

    unit = Unit(id=1)
    research_group = ResearchGroup()
    research_group.id = 2
    unit.research_groups = [research_group]
    unit_repository.save(unit)

    remove_research_group(1, 2)

    assert research_group.status == 'DELETED'


def test_remove_survey():
    research_group_repository = ResearchGroupRepository()
    repository = {'ResearchGroupRepository': research_group_repository,
                  'SurveyRepository': SurveyRepository()}
    configure(repository)

    survey = Survey()
    survey.id = 2

    research_group = ResearchGroup(unit_id=1)
    research_group.id = 1
    research_group.surveys = [survey]
    research_group_repository.save(research_group)

    remove_survey(1, 2)

    assert survey.status == 'DELETED'


def test_remove_question():
    question_repository = QuestionRepository()
    survey_repository = SurveyRepository()
    repository = {'QuestionRepository': question_repository,
                  'SurveyRepository': survey_repository}
    configure(repository)

    question = Question()
    question.id = 2

    survey = Survey()
    survey.id = 1
    survey.questions = [question]
    survey_repository.save(survey)

    remove_question(1, 2)

    assert question.status == 'DELETED'


def test_remove_response():
    response_repository = ReponseRepository()
    question_repository = QuestionRepository()
    repository = {'QuestionRepository': question_repository,
                  'ReponseRepository': response_repository}
    configure(repository)

    response = Response()
    response.id = 2

    question = Question()
    question.id = 1
    question.responses = [response]
    question_repository.save(question)

    remove_response(1, 2)

    assert response.status == 'DELETED'
