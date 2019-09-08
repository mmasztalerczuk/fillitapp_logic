from bussineslogic.mobi_logic.aggregations.organization.domain.entities.research_group import \
    ResearchGroup

from bussineslogic.mobi_logic.aggregations.organization.services.organization_service import OrganizationService


def test_get_research_groups(mocker):
    package = 'bussineslogic.mobi_logic.aggregations.organization.services.organization_service.get_repository'

    rs_1 = ResearchGroup(unit_id="1")
    rs_2 = ResearchGroup(unit_id="1")
    rs_3 = ResearchGroup(unit_id="1")
    rs_3.status = ResearchGroup.STATUS.DELETED

    unit_mock = mocker.Mock()
    unit_mock.research_groups = [rs_1, rs_2, rs_3]

    unit_repository = mocker.Mock()
    unit_repository.get_unit.return_value = unit_mock

    get_repository_mock = mocker.patch(package)
    get_repository_mock.return_value = unit_repository

    ans = OrganizationService.get_research_groups("0", "1")

    assert ans == [rs_1, rs_2]
