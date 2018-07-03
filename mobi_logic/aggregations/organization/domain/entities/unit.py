import logging

import uuid
from sqlalchemy import Column, String, Integer
from taranis.abstract import DomainEvent, Entity, Factory
from taranis import publish



logger = logging.getLogger(__name__)
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)


Base = declarative_base()


class Unit(Base):
    """The unit that represents the highest organizational unit in the hierarchy.

       He is responsible for the creation of new research groups and is the place that determines
       the researcher's affiliation
    """
    __tablename__ = 'unit'
    id = Column(String(80), primary_key=True)
    aggregate_id = Column(String(80), primary_key=True)
    user_id = Column(String(80), nullable=False)
    name = Column(String(120), nullable=False)
    code = Column(String(120), nullable=False)
    description = Column(String(120), nullable=False)

    def __init__(self, id=None, aggregate_id=None, user_id=None, name=None, code=None, description=None):
        self.id = id
        self.aggregate_id = aggregate_id
        self.user_id = user_id
        self.name = name
        self.code = code
        self.description = description

    class Created(DomainEvent):
        type = "Unit.Created"

    class CreatedResearchGroup(DomainEvent):
        type = "Unit.CreatedResearchGroup"

    def configure(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        if 'code' in kwargs:
            self.code = kwargs['code']
        else:
            self.code = "ABCDEF"

        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = ""

        self.name = kwargs['name']
        self.user_id = kwargs['user_id']

        event = Unit.Created(id=self.id,
                             aggregate_id=self.id,
                             user_id=self.user_id,
                             name=self.name,
                             code=self.code,
                             description=self.description,
                             parent=Unit)
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
        event = Unit.CreatedResearchGroup(id=str(uuid.uuid4()),
                                          aggregate_id=self.id,
                                          name=name,
                                          code=code,
                                          description=description,
                                          parent=Unit)

        publish(event)


class UnitFactory(Factory):
    """Unit factory"""

    def build(self, user_id, data):
        logger.debug("Building new unit")

        unit = Unit()
        unit.configure(user_id=user_id,
                       name=data['name'],
                       description=data['description'])

        logger.debug("Finished building new unit id: {unit.id}")
        return unit