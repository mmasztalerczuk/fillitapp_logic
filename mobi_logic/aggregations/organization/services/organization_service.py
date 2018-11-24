from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup
from mobi_logic.aggregations.organization.domain.entities.unit import Unit


class OrganizationService:

    @staticmethod
    def get_units(user_id):
        UnitRepository = get_repository('UnitRepository')
        units = UnitRepository.get_all_units(user_id)
        filtered_units = []

        for unit in units:
            filtered_research_group = []
            for rs in unit.research_groups:
                if rs.status != ResearchGroup.STATUS.DELETED:
                    filtered_research_group.append(rs)
            unit.research_groups = filtered_research_group
            filtered_units.append(unit)

        return filtered_units

    @staticmethod
    def get_research_group(user_id, unit_id, research_group_id):
        UnitRepository = get_repository('UnitRepository')
        unit = UnitRepository.get_unit(user_id, unit_id)
        return unit.get_research_group(research_group_id)

    @staticmethod
    def update_research_group(user_id, unit_id, research_group_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)
        rs = unit.get_research_group(research_group_id)

        rs.update_values(data)


    @staticmethod
    def create_unit(user_id, data):
        UnitRepository = get_repository('UnitRepository')
        unit = Unit()
        unit.configure(user_id=user_id,
                       name=data['name'],
                       description=data['description'])

        UnitRepository.save(unit)
        return unit

    @staticmethod
    def create_research_group(user_id, unit_id, data):
        UnitRepository = get_repository('UnitRepository')

        unit = UnitRepository.get_unit(user_id, unit_id)

        unit.create_research_group(data['name'],
                                   code=data.get('code'),
                                   description=data.get('description'))

        return unit
