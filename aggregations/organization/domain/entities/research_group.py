import logging

import uuid

from abstract.enities import Entity
from abstract.factory import Factory
from aggregations.polls.domain.survey import SurveyFactory

logger = logging.getLogger(__name__)


class ResearchGroup(Entity):

    def create_new_survey(self, name):
        return SurveyFactory.build(name)


class ResearchGroupFactory(Factory):
    """New Research Group Factory"""

    @staticmethod
    def build(name):
        logger.debug("Building new research group unit")
        unit = ResearchGroup(uuid.uuid4(), name, None)
        logger.debug(f"Finished building new research group id: {unit.id}")
        return unit
