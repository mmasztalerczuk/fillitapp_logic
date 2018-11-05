import uuid
from taranis import publish
from taranis.abstract import Factory, DomainEvent
import logging

logger = logging.getLogger(__name__)


class Respondent():
    class Created(DomainEvent):
        type = "Respondent.Created"

    class NewResponse(DomainEvent):
        type = "NewResponse.Created"

    def add_response(self, questions):
        event_id = str(uuid.uuid4())

        for question in questions:
            event = Respondent.NewResponse(id=event_id,
                                           question_id=question['id'],
                                           response_id=question['response'],
                                           aggregate_id=event_id)

            publish(event)


class RespondentFactory(Factory):
    """Respondent factory"""

    def build(self, data):
        logger.debug("Building new unit")

        event_id = str(uuid.uuid4())

        event = Respondent.Created(id=event_id,
                                   device_id=data['device_id'],
                                   aggregate_id=event_id)

        publish(event)
