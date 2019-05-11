import datetime
import uuid
from taranis import publish
from taranis.abstract import Factory, DomainEvent
import logging

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.answer import Answer
from mobi_logic.aggregations.organization.domain.entities.answer_text import AnswerText

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
    def create_new(device_id):
        RespondentRepository = get_repository('RespondentRepository')

        respondent = Respondent()
        respondent.device_id = device_id

        RespondentRepository.save(respondent)

        return respondent

    @staticmethod
    def add_response(question_id, responses_id, user_id, text=None):
        AnswerRepository = get_repository('AnswerRepository')
        AnswerTextRepository = get_repository('AnswerTextRepository')
        QuestionRepository = get_repository('QuestionRepository')

        qr = QuestionRepository.get_by_id(question_id)
        if qr.type == 'text':
            answer = AnswerText()

            answer.id = str(uuid.uuid4())
            answer.question_id = question_id
            answer.ids = None
            answer.user_id = user_id
            answer.date = datetime.datetime.now()
            answer.text = text

            AnswerTextRepository.save(answer)

        else:
            for response_id in responses_id:
                answer = Answer()

                answer.id = str(uuid.uuid4())
                answer.ids = None
                answer.response_id = response_id
                answer.question_id = question_id
                answer.user_id = user_id
                answer.date = datetime.datetime.now()

                AnswerRepository.save(answer)

