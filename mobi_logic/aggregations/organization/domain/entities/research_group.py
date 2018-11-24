import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.survey import Survey


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

    def create_survey(self, name):
        event = Survey.Created(id=str(uuid.uuid4()),
                               name=name,
                               aggregate_id=self.id)

        publish(event)

    def update_values(self, data):
        ResearchGroupRepository = get_repository('ResearchGroupRepository')

        if data['status'] and data['status'] == ResearchGroup.STATUS.STARTED:
            self.status = data['status']

        ResearchGroupRepository.save(self)

    def remove_survey(self, survey_id):
        for survey in self.surveys:
            if survey.id == survey_id:
                survey.status = ResearchGroup.STATUS.DELETED
                self.survey_repository.save(survey)
                break

        # @TODO throw exception on missing survey
