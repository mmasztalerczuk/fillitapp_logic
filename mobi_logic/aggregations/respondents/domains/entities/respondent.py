import datetime
import uuid
from taranis import publish
from taranis.abstract import Factory, DomainEvent
import logging

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.answer import Answer

logger = logging.getLogger(__name__)


class Respondent:
    class Created(DomainEvent):
        type = "Respondent.Created"

    class NewResponse(DomainEvent):
        type = "NewResponse.Created"

    def __init__(self):
        self.id = str(uuid.uuid4())

    @staticmethod
    def get_by_id(device_id):
        RespondentRepository = get_repository('RespondentRepository')
        return RespondentRepository.get_by_device_id(device_id)

    @staticmethod
    def create_new(device_id, code):
        RespondentRepository = get_repository('RespondentRepository')

        respondent = Respondent()
        respondent.device_id = device_id
        respondent.code = code

        RespondentRepository.save(respondent)

    @staticmethod
    def add_response(question_id, response_id, device_id):


        AnswerRepository = get_repository('AnswerRepository')
        answer = Answer()

        answer.id = str(uuid.uuid4())
        answer.response_id = response_id
        answer.question_id = question_id
        answer.device_id = device_id
        answer.date = datetime.datetime.now()


        AnswerRepository.save(answer)


    # def add_response(self, questions):
    #     event_id = str(uuid.uuid4())
    #
    #     for question in questions:
    #         event = Respondent.NewResponse(id=event_id,
    #                                        question_id=question['id'],
    #                                        response_id=question['response'],
    #                                        aggregate_id=event_id)
    #
    #         publish(event)



