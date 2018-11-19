from mobi_logic import get_repository


def remove_research_group(unit_id, research_group_id):
    UnitRepository = get_repository('UnitRepository')

    unit = UnitRepository.get_unit(unit_id)

    unit.remove_research_group_id(research_group_id)
