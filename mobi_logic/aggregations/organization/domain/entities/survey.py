import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.question import Question
from mobi_logic.aggregations.organization.domain.entities.response import Response


class Survey:

    @property
    def survey_repository(self):
        return get_repository('QuestionRepository')

    class Created(DomainEvent):
        type = "Survey.Created"

    def add_question(self, name, type, responses):
        new_question_id = str(uuid.uuid4())
        event = Question.Created(id=new_question_id,
                                 name=name,
                                 type=type,
                                 aggregate_id=self.id)

        publish(event)

        for response in responses:
            event = Response.Created(id=str(uuid.uuid4()),
                             value=response['value'],
                             type=response['type'],
                             aggregate_id=new_question_id)

            publish(event)

    def remove_question(self, question_id):
        for question in self.questions:
            if question.id == question_id:
                question.status = 'DELETED'
                self.survey_repository.save(question)
                break

        # @TODO throw exception on missing survey

