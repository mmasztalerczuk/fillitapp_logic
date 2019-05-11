import uuid
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.response import Response
from mobi_logic.aggregations.organization.exceptions.errors import ResponseNotFound


class Question:

    class STATUS:
        NEW = 'new'
        DELETED = 'deleted'
        STARTED = 'started'


    @property
    def repository(self):
        return get_repository('QuestionRepository')

    class Created(DomainEvent):
        type = "Question.Created"

    def create_response(self, value, type):
        ResponseRepository = get_repository('ResponseRepository')

        response = Response()

        response.id = str(uuid.uuid4())
        response.ids = None
        response.question_id = self.id
        response.value = value
        response.type = type
        response.status = Question.STATUS.NEW

        ResponseRepository.save(response)

        return response.id

    def get_response(self, response_id, deleted=False):
        for response in self.responses:
            if response.id == response_id:
                if not deleted and response.status != Response.STATUS.DELETED:
                    return response
                raise ResponseNotFound
        raise ResponseNotFound

    def update_values(self, data):
        QuestionRepository = get_repository('QuestionRepository')

        if data.get('status') and data['status'] == Question.STATUS.STARTED:
            self.status = data['status']

        if data.get('type'):
            self.type = data['type']

        if data.get('name'):
            self.name = data['name']

        QuestionRepository.save(self)

    def remove_response(self, response_id):
        ResponseRepository = get_repository('ResponseRepository')
        for response in self.responses:
            if response.id == response_id:
                response.status = Response.STATUS.DELETED
                ResponseRepository.save(response)
                break

        # @TODO throw exception on missing survey
