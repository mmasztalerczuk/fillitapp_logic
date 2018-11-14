import logging
from taranis.abstract import DomainEvent


logger = logging.getLogger(__name__)


class User:
    class Created(DomainEvent):
        type = "User.Created"



