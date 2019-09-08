from mobi_logic.aggregations.organization.services.research_group_service import remove_survey

from mobi_logic.aggregations.organization.services.research_group_service import \
    get_research_group_license

def test_remove_research_group(mocker):
    package = 'mobi_logic.aggregations.organization.services.research_group_service.get_repository'
    research_group_id = 1
    survey_group_id = 2
    unit_id = 0
    user_id = "ABC"

    research_group = mocker.Mock()

    unit_mock = mocker.Mock()
    unit_mock.get_unit.return_value = research_group

    get_repository_mock = mocker.patch(package)
    get_repository_mock.return_value = unit_mock

    assert remove_survey(user_id, unit_id, research_group_id, survey_group_id) is None

    get_repository_mock.assert_called_once_with('UnitRepository')
    unit_mock.get_unit.assert_called_once_with(user_id, unit_id)


def test_get_research_group_license(mocker):
    package = 'mobi_logic.aggregations.organization.services.research_group_service.get_repository'
    research_group_code = "ABCDEF"
    license = "my license"

    research_group = mocker.Mock()
    research_group.license = license

    research_group_repository_mock = mocker.Mock()
    research_group_repository_mock.get_by_code.return_value = research_group

    get_repository_mock = mocker.patch(package)
    get_repository_mock.return_value = research_group_repository_mock

    assert get_research_group_license(research_group_code) == license

    get_repository_mock.assert_called_once_with('ResearchGroupRepository')
    research_group_repository_mock.get_by_code.assert_called_once_with(research_group_code)
