import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.response import Response


class Question:

    @property
    def question_repository(self):
        return get_repository('QuestionRepository')

    class Created(DomainEvent):
        type = "Question.Created"

    def create_responses(self, value, type, question_id):
        event = Response.Created(id=str(uuid.uuid4()),
                               value=value,
                               type=type,
                               aggregate_id=question_id)

        publish(event)

    def remove_response(self, response_id):
        for response in self.responses:
            if response.id == response_id:
                response.status = 'DELETED'
                self.question_repository.save(response)
                break

        # @TODO throw exception on missing survey
