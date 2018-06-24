from mobi_logic.aggregations.organization.domain import UnitFactory


def create_new_unit(name):
    return UnitFactory.build(name)

