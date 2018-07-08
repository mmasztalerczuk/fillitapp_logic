from mobi_logic.aggregations.organization.domain.entities.unit import Unit, ResearchGroup


def test_unit_create_research_group(mocker):
    event_store = []

    def publish_mock(event):
        event_store.append(event)

    mocker.patch("mobi_logic.aggregations.organization"
                 ".domain.entities.unit.publish",
                 publish_mock)

    name = "Unit name"
    code = "Code Name"
    description = "Description Name"

    unit = Unit()
    unit.create_research_group(name, code, description)

    assert 1 == len(event_store)
    event = event_store[0]

    assert ResearchGroup.Created == type(event)
    assert name == event.name
    assert code == event.code
    assert description == event.description
