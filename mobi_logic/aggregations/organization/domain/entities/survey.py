import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.question import Question
from mobi_logic.aggregations.organization.exceptions.errors import QuestionNotFound


class Survey:

    class STATUS:
        NEW = 'new'
        DELETED = 'deleted'
        STARTED = 'started'


    @property
    def survey_repository(self):
        return get_repository('QuestionRepository')

    class Created(DomainEvent):
        type = "Survey.Created"

    def create_question(self, name, type):
        QuestionRepository = get_repository('QuestionRepository')

        question = Question()

        question.id=str(uuid.uuid4())
        question.survey_id = self.id
        question.unit_id = self.unit_id
        question.name=name
        question.type = type
        question.status = Question.STATUS.NEW

        QuestionRepository.save(question)

    def get_question(self, question_id, deleted=False):
        for question in self.questions:
            if question.id == question_id:
                if not deleted and question.status != Question.STATUS.DELETED:
                    return question
                raise QuestionNotFound
        raise QuestionNotFound

    def remove_question(self, question_id):
        for question in self.questions:
            if question.id == question_id:
                question.status = Question.STATUS.DELETED
                self.survey_repository.save(question)
                break

        # @TODO throw exception on missing survey

    def update_values(self, data):
        SurveyRepository = get_repository('SurveyRepository')

        if data.get('status') and data['status'] == Survey.STATUS.STARTED:
            self.status = data['status']

        if data.get('startdate'):
            self.startdate = data.get('startdate')

        if data.get('enddate'):
            self.enddate = data['enddate']

        if data.get('description'):
            self.description = data['description']

        if data.get('name'):
            self.name = data['name']

        SurveyRepository.save(self)