from .aggregations.organization.repositories.unit import UnitRepository
from .aggregations.organization.domain.entities.unit import UnitFactory

event_queue = None
event_subscriber = None

def install(event_subscriber, event_queue):
    event_queue = event_queue
