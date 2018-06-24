import logging

import uuid

from taranis.abstract import Entity, Factory
from mobi_logic.aggregations.polls.domain.question import QuestionFactory

logger = logging.getLogger(__name__)


class Survey(Entity):

    def create_new_question(self, name):
        return QuestionFactory(name)


class SurveyFactory(Factory):
    """Unit factory"""

    @staticmethod
    def build(name):
        logger.debug("Building new question")
        survey = Survey(uuid.uuid4(), name, None)
        logger.debug("Finished building new question id: {unit.id}")
        return survey