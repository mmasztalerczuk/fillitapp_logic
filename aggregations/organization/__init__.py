from aggregations.organization.domain.entities.unit import UnitFactory


def create_new_unit(name):
    return UnitFactory.build(name)

