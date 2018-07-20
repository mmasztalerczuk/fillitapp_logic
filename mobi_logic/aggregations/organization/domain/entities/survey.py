from sqlalchemy.ext.declarative import declarative_base
from taranis.abstract import DomainEvent

Base = declarative_base()


class Survey():
    class Created(DomainEvent):
        type = "Survey.Created"
