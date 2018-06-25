from taranis.abstract.repository import Repository


class UnitRepository(Repository):

    def save_all(self):
        for event in self._event_queue.get_events():
            self.put(event)
        self._event_queue.clear()

    def put(self, unit):
        self._persistent_storage.append(unit)

    def get_all(self):
        data = []

        for event in self._persistent_storage.get_all():
            if event['type'] == "Unit.Created":
                data.append({'aggregate_id': event['aggregate_id'],
                             'name': event['name'],
                             'code': event['code'],
                             'description': event['description']})
        return data
