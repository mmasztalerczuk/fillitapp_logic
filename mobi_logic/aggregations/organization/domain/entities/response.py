from taranis.abstract import DomainEvent

from mobi_logic import get_repository


class Response:

    class STATUS:
        NEW = 'new'
        DELETED = 'deleted'
        STARTED = 'started'

    class Created(DomainEvent):
        type = "Response.Created"


    def update_values(self, data):
        ResponseRepository = get_repository('ResponseRepository')

        if data.get('status') and data['status'] == Response.STATUS.STARTED:
            self.status = data['status']

        if data.get('type'):
            self.type = data['type']

        if data.get('value'):
            self.value = data['value']

        ResponseRepository.save(self)
