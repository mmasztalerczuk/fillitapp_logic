from mobi_logic import UnitRepository
from mobi_logic.aggregations.organization.domain.entities.unit import Unit


def test_unit_create_research_group(mocker):
    event_store = []

    def publish_mock(event):
        event_store.append(event)

    mocker.patch("mobi_logic.aggregations.organization.domain.entities.unit.publish", publish_mock)

    # event_store = []

    class MockRepository:
        def get(self, clazz, id):
            if clazz == Unit:
                unit = Unit()
                unit._id = id
                return unit

    unit_id = 1
    unit = UnitRepository(MockRepository()).get(unit_id)
    research_group = unit.create_research_group("Moja grupa 1")

    assert type(event_store[0]) == Unit.CreatedResearchGroup
    