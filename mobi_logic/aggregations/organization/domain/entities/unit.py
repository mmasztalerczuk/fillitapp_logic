import logging
import uuid
from functools import singledispatch

from taranis.abstract import DomainEvent, Entity, Factory
from taranis import publish

logger = logging.getLogger(__name__)


class Unit(Entity):
    """The unit that represents the highest organizational unit in the hierarchy.

       He is responsible for the creation of new research groups and is the place that determines
       the researcher's affiliation
    """

    class Created(DomainEvent):
        type = "Unit.Created"

    class CreatedResearchGroup(DomainEvent):
        pass

    def configure(self, *args, **kwargs):
        super().configure(*args)
        if 'code' in kwargs:
            self.code = kwargs['code']
        else:
            self.code = "ABCDEF"

        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = ""

        event = Unit.Created(aggregate_id=self._id,
                             name=self.name,
                             code=self.code,
                             description=self.description)
        publish(event)


    def create_research_group(self, name, code=None, description=None):
        """
        Creates a new research group. The process of creating a new group requires a name.
        The name will be visible to participants of the study.
        Each research group is recognized by the participants of the study by means of a code.
        This code can be given manually, but it can also be generated randomly.

        Args:
            name (str): The name of new research group. This will be visible for participants
            code (str, optional): This code which will be use to join to research group by participants.
            description (str, optional): The description of research group. This will be visible for participants.

        Returns:
            New created research group

        Raises:
            None
        """
        event = Unit.CreatedResearchGroup(aggregate_id=self._id,
                                          name=name,
                                          code=code,
                                          description=description)

        publish(event)


    @singledispatch
    def _when(self, event):
        pass


class UnitFactory(Factory):
    """Unit factory"""

    @staticmethod
    def build(name):
        logger.debug("Building new unit")

        unit = Unit()
        unit.configure(str(uuid.uuid4()), name)

        logger.debug("Finished building new unit id: {unit.id}")
        return unit