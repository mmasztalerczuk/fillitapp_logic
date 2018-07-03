from taranis.abstract.repository import Repository

from mobi_logic.aggregations.organization.domain.entities.unit import Unit


class UnitRepository(Repository):

    def __init__(self, persistent_storage, user_id):
        super(UnitRepository, self).__init__(persistent_storage)
        self._user_id = user_id

    def get(self, unit_id):
        properties = {'user_id': self._user_id, 'aggregate_id': unit_id}
        return self._persistent_storage.get(Unit, properties)[0]

    def get_all(self):
        properties = {'user_id': self._user_id}
        return self._persistent_storage.get(Unit, properties)
