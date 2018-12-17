from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup


def test_research_group_remove(mocker):
    package = 'mobi_logic.aggregations.organization.domain.entities.research_group.get_repository'

    repository_mock = mocker.Mock()

    get_repository_mock = mocker.patch(package)
    get_repository_mock.return_value = repository_mock

    survey_id = 1
    unit_id = 1
    s1, s2, s3 = mocker.Mock(), mocker.Mock(), mocker.Mock()
    s1.id = survey_id

    surveys_list = [s1, s2, s3]

    research_group = ResearchGroup(unit_id)
    research_group.surveys = surveys_list

    research_group.remove_survey(survey_id)

    get_repository_mock.assert_called_once_with('SurveyRepository')
    repository_mock.save.assert_called_once_with(s1)
