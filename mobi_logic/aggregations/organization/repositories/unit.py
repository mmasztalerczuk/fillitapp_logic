from taranis.abstract.repository import Repository

from mobi_logic.aggregations.organization.domain.entities.unit import Unit


class UnitRepository(Repository):

    def __init__(self, persistent_storage, user_id):
        super(UnitRepository, self).__init__(persistent_storage)
        self._user_id = user_id

    def get(self, unit_id):
        data = self._persistent_storage.get(self._user_id, unit_id)
        unit = Unit()
        del data['type']

        for key in data.keys():
            setattr(unit, key, data[key])

        return unit

    def get_all(self):
        data = []

        for event in self._persistent_storage.get_all(self._user_id):
            if event['type'] == "Unit.Created":
                del event['type']
                unit = Unit()
                for key in event.keys():
                    setattr(unit, key, event[key])
                data.append(unit)
        return data
