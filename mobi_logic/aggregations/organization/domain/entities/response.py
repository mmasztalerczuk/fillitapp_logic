from taranis.abstract import DomainEvent


class Response():
    class Created(DomainEvent):
        type = "Response.Created"
