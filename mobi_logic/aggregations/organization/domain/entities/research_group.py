import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic.aggregations.organization.domain.entities.survey import Survey


class ResearchGroup():
    class Created(DomainEvent):
        type = "ResearchGroup.Created"

    class AddRespondent(DomainEvent):
        type = "ResearchGroup.AddRespondent"

    def create_survey(self, name):
        event = Survey.Created(id=str(uuid.uuid4()),
                               name=name,
                               aggregate_id=self.id)

        publish(event)

