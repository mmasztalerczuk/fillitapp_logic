from taranis.abstract import DomainEvent


class Question():
    class Created(DomainEvent):
        type = "Question.Created"
