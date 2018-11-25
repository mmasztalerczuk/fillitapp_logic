import datetime
import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.survey import Survey
from mobi_logic.aggregations.organization.exceptions.errors import SurveyNotFound


class ResearchGroup:

    class STATUS:
        NEW = "new"
        STARTED = "started"
        FINISHED = "finished"
        DELETED = "deleted"

        VALUES = [NEW, STARTED, FINISHED, DELETED]

    @property
    def survey_repository(self):
        return get_repository('SurveyRepository')

    class Created(DomainEvent):
        type = "ResearchGroup.Created"

    class AddRespondent(DomainEvent):
        type = "ResearchGroup.AddRespondent"

    def create_survey(self, name, description=None):
        SurveyRepository = get_repository('SurveyRepository')

        survey = Survey()

        survey.id=str(uuid.uuid4())
        survey.research_group_id = self.id
        survey.unit_id = self.unit_id
        survey.name=name
        survey.status = ResearchGroup.STATUS.NEW
        survey.description=description
        survey.startdate = None
        survey.enddate = None

        SurveyRepository.save(survey)

    def get_survey(self, survey_id, deleted=False):
        for survey in self.surveys:
            if survey.id == survey_id:
                if not deleted and survey.status != Survey.STATUS.DELETED:
                    return survey
                raise SurveyNotFound
        raise SurveyNotFound

    def update_values(self, data):
        ResearchGroupRepository = get_repository('ResearchGroupRepository')

        if data.get('status') and data['status'] == ResearchGroup.STATUS.STARTED:
            self.status = data['status']

        if data.get('startdate'):
            self.startdate = data.get('startdate')

        if data.get('enddate'):
            self.enddate = data['enddate']

        if data.get('description'):
            self.description = data['description']

        if data.get('name'):
            self.name = data['name']

        if data.get('code'):
            self.code = data['code']

        ResearchGroupRepository.save(self)

    def remove_survey(self, survey_id):
        for survey in self.surveys:
            if survey.id == survey_id:
                survey.status = ResearchGroup.STATUS.DELETED
                self.survey_repository.save(survey)
                break

        # @TODO throw exception on missing survey
