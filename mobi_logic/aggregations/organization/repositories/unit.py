from taranis.abstract.repository import Repository

from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup
from mobi_logic.aggregations.organization.domain.entities.unit import Unit


class UnitRepository(Repository):

    def __init__(self, persistent_storage, user_id):
        super(UnitRepository, self).__init__(persistent_storage)
        self._user_id = user_id

    def get(self, unit_id):
        data = []
        events = {}
        for event in self._persistent_storage.get(self._user_id, unit_id):
            print("evendt", event)
            if event['type'] == "Unit.Created":
                del event['type']
                if 'research_groups' not in event:
                    event['research_groups'] = {}

                events[event['id']] = event

            elif event['type'] == "Unit.CreatedResearchGroup":
                del event['type']
                events[event['aggregate_id']].research_groups[event['id']] = event
        print("fin")
        #print("here", events)
        unit = Unit()
        for item in events.values():

            for key in item.keys():
                if key == "research_groups":
                    unit.research_groups = []
                    for i in item[key].values():
                        research_group = ResearchGroup()
                        for val in i.keys():
                            setattr(research_group, val, i[val])
                        unit.research_groups.append(research_group)
                else:
                    setattr(unit, key, item[key])
            data.append(unit)
        #print(data)
        return unit

    def get_all(self):
        data = []
        events = {}
        for event in self._persistent_storage.get_all(self._user_id):
            print("event", event)
            if event['type'] == "Unit.Created":
                del event['type']
                if 'research_groups' not in event:
                    event['research_groups'] = {}

                events[event['id']] = event

            elif event['type'] == "Unit.CreatedResearchGroup":
                del event['type']
                events[event['aggregate_id']].research_groups[event['id']] = event

        print(events)
        for item in events.values():
            unit = Unit()

            for key in item.keys():
                if key == "research_groups":
                    unit.research_groups = []
                    for i in item[key].values():
                        research_group = ResearchGroup()
                        for val in i.keys():
                            setattr(research_group, val, i[val])
                        unit.research_groups.append(research_group)
                else:
                    setattr(unit, key, item[key])
            data.append(unit)
        print(data)
        return data
