import logging

import uuid

from abstract.enities import Entity
from abstract.factory import Factory

logger = logging.getLogger(__name__)


class Question(Entity):
    pass


class QuestionFactory(Factory):
    """Unit factory"""

    @staticmethod
    def build(name):
        logger.debug("Building new question")
        unit = Question(uuid.uuid4(), name)
        logger.debug("Finished building new question id: {unit.id}")
        return unit