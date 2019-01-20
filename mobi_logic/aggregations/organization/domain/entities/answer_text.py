import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic.aggregations.organization.domain.entities.response import Response


class AnswerText():
    class Created(DomainEvent):
        type = "AnswerText.Created"

