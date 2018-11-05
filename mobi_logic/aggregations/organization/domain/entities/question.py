import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic.aggregations.organization.domain.entities.response import Response


class Question():
    class Created(DomainEvent):
        type = "Question.Created"

    def create_responses(self, value, type, question_id):
        event = Response.Created(id=str(uuid.uuid4()),
                               value=value,
                               type=type,
                               aggregate_id=question_id)

        publish(event)
