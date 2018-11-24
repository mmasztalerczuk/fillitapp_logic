import logging
import random
import string
import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup
from mobi_logic.aggregations.organization.exceptions.errors import ResearchGroupNotFound

logger = logging.getLogger(__name__)


class Unit:
    """The unit that represents the highest organizational unit in the hierarchy.

       He is responsible for the creation of new research groups and is the place that determines
       the researcher's affiliation
    """
    def __init__(self, id=None, aggregate_id=None, user_id=None, name=None, code=None, description=None):
        self.id = id
        self.aggregate_id = aggregate_id
        self.user_id = user_id
        self.name = name
        self.code = code
        self.description = description

    class Created(DomainEvent):
        type = "Unit.Created"

    def remove_research_group_id(self, research_group_id):
        ResearchGroupRepository = get_repository('ResearchGroupRepository')
        for rs in self.research_groups:
            if rs.id == research_group_id:
                rs.status = ResearchGroup.STATUS.DELETED
                ResearchGroupRepository.save(rs)

        # @TODO throw no founded rs

    def get_research_group(self, research_group_id, deleted=False):
        for rs in self.research_groups:
            if rs.id == research_group_id:
                if not deleted and rs.status != ResearchGroup.STATUS.DELETED:
                    return rs
                raise ResearchGroupNotFound
            raise ResearchGroupNotFound

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

    def add_respondent(self, respondent_id, research_group_id):
        event = ResearchGroup.AddRespondent(id=str(uuid.uuid4()),
                                            user_id=respondent_id,
                                            research_group_id=research_group_id,
                                            aggregate_id=self.id)

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
        if code is None:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        ResearchGroupRepository = get_repository('ResearchGroupRepository')

        research_group = ResearchGroup()

        research_group.id=str(uuid.uuid4())
        research_group.aggregate_id=self.id
        research_group.name=name
        research_group.code=code
        research_group.status = ResearchGroup.STATUS.NEW
        research_group.description=description
        research_group.user_id=self.user_id
        research_group.parent=ResearchGroup

        ResearchGroupRepository.save(research_group)
