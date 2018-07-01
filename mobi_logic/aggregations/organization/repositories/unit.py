from taranis.abstract.repository import Repository


class UnitRepository(Repository):

    def __init__(self, persistent_storage, user_id):
        super(UnitRepository, self).__init__(persistent_storage)
        self._user_id = user_id

    def get(self, unit_id):
        return self._persistent_storage.get(self._user_id, unit_id)

    def get_all(self):
        data = []

        for event in self._persistent_storage.get_all(self._user_id):
            if event['type'] == "Unit.Created":
                data.append({'aggregate_id': event['aggregate_id'],
                             'name': event['name'],
                             'code': event['code'],
                             'description': event['description']})
        return data
