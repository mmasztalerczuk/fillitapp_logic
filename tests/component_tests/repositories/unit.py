class UnitRepository:
    def __init__(self):
        self._units = {}

    def get_unit(self, unit_id):
        if unit_id in self._units:
            return self._units[unit_id]

    def save(self, unit):
        self._units[unit.id] = unit
