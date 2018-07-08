import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def event_store(mocker):
    logger.debug("Creating event_store")
    store = []

    def publish_mock(event):
        store.append(event)

    mocker.patch("mobi_logic.aggregations.organization.domain.entities.unit.publish", publish_mock)

    yield store
