from taranis.abstract.repository import Repository

from mobi_logic.aggregations.organization.domain.entities.unit import Unit, ResearchGroup


class UnitRepository(Repository):

    def __init__(self, persistent_storage, user_id):
        super(UnitRepository, self).__init__(persistent_storage)
        self._user_id = user_id

    def get_research_group(self, unit_id, research_group_id):
        properties = (ResearchGroup.user_id == self._user_id,
                      ResearchGroup.aggregate_id == unit_id,
                      ResearchGroup.id == research_group_id)
        return self._persistent_storage.get(ResearchGroup, properties)[0]

    def get(self, unit_id):
        properties = (Unit.user_id == self._user_id, Unit.aggregate_id == unit_id)
        return self._persistent_storage.get(Unit, properties)[0]

    def get_all(self):
        properties = (Unit.user_id == self._user_id,)
        return self._persistent_storage.get(Unit, properties)
