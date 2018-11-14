from .aggregations.organization.repositories.unit import UnitRepository
from .aggregations.organization.domain.entities.unit import UnitFactory

repos = {}


def get_repository(name):
    if name not in repos:
        raise NotImplemented
    return repos[name]


def configure(repositories):
    global repos
    repos = repositories
