from mobi_logic.aggregations.organization.services.research_group_service import remove_survey


def test_remove_research_group(mocker):
    package = 'mobi_logic.aggregations.organization.services.research_group_service.get_repository'
    research_group_id = 1
    survey_group_id = 2

    research_group = mocker.Mock()

    repository_mock = mocker.Mock()
    repository_mock.get_research_group.return_value = research_group

    get_repository_mock = mocker.patch(package)
    get_repository_mock.return_value = repository_mock

    assert remove_survey(research_group_id, survey_group_id) is None

    get_repository_mock.assert_called_once_with('ResearchGroupRepository')
    repository_mock.get_research_group.assert_called_once_with(research_group_id)
    research_group.remove_survey.assert_called_once_with(survey_group_id)
