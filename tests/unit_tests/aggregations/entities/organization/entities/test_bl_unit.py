from datetime import timedelta, datetime

from mobi_logic.aggregations.organization.domain.entities.unit import Unit


def test_check_only_minutes():
    dateA = datetime(2012, 3, 3, 6, 6, 0, 0)
    dateB = datetime(2012, 3, 3, 23, 6, 0, 0)
    delta = timedelta(seconds=60*60)

    assert Unit.get_check_only_minutes(dateA, dateB, delta)
