import uuid
from sqlalchemy.ext.declarative import declarative_base
from taranis import publish
from taranis.abstract import DomainEvent
from mobi_logic.aggregations.organization.domain.entities.question import Question
Base = declarative_base()


class Survey():
    class Created(DomainEvent):
        type = "Survey.Created"

    def add_question(self, name):
        event = Question.Created(id=str(uuid.uuid4()),
                                 name=name,
                                 aggregate_id=self.id)

        publish(event)
