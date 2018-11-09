import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic.aggregations.organization.domain.entities.response import Response


class Answer():
    class Created(DomainEvent):
        type = "Answer.Created"

    def create_answer(self, device_id, response_id):
        event = Answer.Created(id=str(uuid.uuid4()),
                               device_id=device_id,
                               response_id=response_id)

        publish(event)
