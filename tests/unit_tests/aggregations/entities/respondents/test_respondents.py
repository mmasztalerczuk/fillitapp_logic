import pytest
from mobi_logic.aggregations.respondents.domains.entities.respondent import Respondent
from mobi_logic.aggregations.respondents.domains.exceptions.errors import RespondentAlreadyRegistered


@pytest.fixture
def repository(mocker):
    package = 'mobi_logic.aggregations.respondents.domains.entities.respondent.get_repository'

    repository_mock = mocker.Mock()

    get_repository_mock = mocker.patch(package)
    get_repository_mock.return_value = repository_mock

    return repository_mock


def disable_test_create_new_respondents(repository):
    device_id = "123456789"
    code = "ABCDEF"
    respondent = Respondent.create_new(device_id, code)
    assert respondent.device_id == device_id
    assert respondent.code == code


def disable_test_create_new_respondents(repository):
    device_id = "123456789"
    code = "ABCDEF"

    vals = {}

    def save_mock(respondent):
        if respondent.device_id in vals:
            if vals[device_id] == respondent.code:
                raise RespondentAlreadyRegistered

        vals[respondent.device_id] = respondent.code

    repository.save = save_mock

    respondent = Respondent.create_new(device_id, code)
    assert respondent.device_id == device_id
    assert respondent.code == code

    with pytest.raises(RespondentAlreadyRegistered):
        Respondent.create_new(device_id, code)


