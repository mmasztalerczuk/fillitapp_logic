# -*- coding: utf-8 -*-
import random
import string
import uuid

from taranis.abstract import DomainEvent
from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.survey import Survey
from mobi_logic.aggregations.organization.exceptions.errors import SurveyNotFound, ResearchGroupDateIncorrect


class ResearchGroup:

    @staticmethod
    def is_code_valid(code):
        if code and len(code) >= 6:
            return True
        return False

    @staticmethod
    def generate_new_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @property
    def new_surveys(self):
        """ Returing only surveys with status NEW"""
        """TODO check maybe we can do that in query?"""
        """TODO is filter is iterator?"""

        return filter(lambda survey: survey.status == Survey.STATUS.NEW, self.surveys)

    def __init__(self, unit_id: str, code: str = None):
        """ Init of research group class.

        This class represents the entities of the research group. Each unit can have many research groups, but there
        can be no research group that does not belong to any unit. Research groups have a survey (one or more)
        that represents specific groups of questions.

        Every created instance of Research Group needs to have an id. At this moment we are using uuid4 to create
        unique value.

        Note:
            Aggregate_id will be saved as unit_id

        Args:
            unit_id (str): The id of unit which is owner of this research group
        """
        self._code = None

        if not ResearchGroup.is_code_valid(code):
            self.code = ResearchGroup.generate_new_code()
        else:
            self.code = code

        # @TODO create function to wrap creation of unique uuid
        self.id = str(uuid.uuid4())

        # @TODO replace aggregate_id with unit_id in model and repository
        self.aggregate_id = unit_id

        # The research group should have a new status as soon as it has been set up.
        self.status = ResearchGroup.STATUS.NEW

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

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
        survey.ids = None
        survey.research_group_id = self.id
        survey.unit_id = self.unit_id
        survey.name=name
        survey.questiondelta = 3600
        survey.status = ResearchGroup.STATUS.NEW
        survey.description=description
        survey.startdate = None
        survey.enddate = None

        SurveyRepository.save(survey)

        return survey

    def get_survey(self, survey_id, deleted=False):
        for survey in self.surveys:
            if survey.id == survey_id:
                if not deleted and survey.status != Survey.STATUS.DELETED:
                    return survey
                raise SurveyNotFound
        raise SurveyNotFound

    def update_values(self, data):
        ResearchGroupRepository = get_repository('ResearchGroupRepository')

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

        if data.get('license'):
            self.license = data['license']

        if data.get('status') and data['status'] == ResearchGroup.STATUS.STARTED:
            self.status = data['status']
            self._validate_research_group()

        ResearchGroupRepository.save(self)

    def _validate_research_group(self):
        if self.startdate is None or self.enddate is None:
            raise ResearchGroupDateIncorrect

        for survey in self.new_surveys:
            if survey.startdate is None or survey.enddate is None:
                raise ResearchGroupDateIncorrect

        #@ TODO better msg and check range

    def remove_survey(self, survey_id):
        for survey in self.new_surveys:
            if survey.id == survey_id:
                survey.status = ResearchGroup.STATUS.DELETED
                self.survey_repository.save(survey)
                break
        else:
            raise SurveyNotFound

    @staticmethod
    def register_response(respondent_id, code):
        RegistrationsRepository = get_repository('RegistrationsRepository')
        ResearchGroupRepository = get_repository('ResearchGroupRepository')

        research_group = ResearchGroupRepository.get_by_code(code)
        RegistrationsRepository.save(research_group.id, respondent_id)
