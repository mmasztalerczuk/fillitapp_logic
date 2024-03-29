import datetime
import logging
import uuid
from taranis import publish
from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.research_group import ResearchGroup
from mobi_logic.aggregations.organization.exceptions.errors import ResearchGroupNotFound

logger = logging.getLogger(__name__)


class Unit:
    """The unit that represents the highest organizational unit in the hierarchy.

       He is responsible for the creation of new research groups and is the place that determines
       the researcher's affiliation
    """
    def __init__(self, id=None, aggregate_id=None, user_id=None, name=None, code=None, description=None):
        self.id = id
        self.aggregate_id = aggregate_id
        self.user_id = user_id
        self.name = name
        self.code = code
        self.description = description

    class Created(DomainEvent):
        type = "Unit.Created"

    def remove_research_group_id(self, research_group_id):
        ResearchGroupRepository = get_repository('ResearchGroupRepository')
        for rs in self.research_groups:
            if rs.id == research_group_id:
                rs.status = ResearchGroup.STATUS.DELETED
                ResearchGroupRepository.save(rs)

        # @TODO throw no founded rs

    def get_research_group(self, research_group_id, deleted=False):
        for rs in self.research_groups:
            if rs.id == research_group_id:

                if not deleted and rs.status != ResearchGroup.STATUS.DELETED:
                    return rs
                raise ResearchGroupNotFound
        raise ResearchGroupNotFound

    def configure(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        if 'code' in kwargs:
            self.code = kwargs['code']
        else:
            self.code = "ABCDEF"

        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = ""

        self.name = kwargs['name']
        self.user_id = kwargs['user_id']

    def add_respondent(self, respondent_id, research_group_id):
        event = ResearchGroup.AddRespondent(id=str(uuid.uuid4()),
                                            user_id=respondent_id,
                                            research_group_id=research_group_id,
                                            aggregate_id=self.id)

        publish(event)

    @staticmethod
    def get_check_only_minutes(dateA, dateB, delta=None):
        if delta is not None:
            dateC = dateB + delta
            if dateB.day < dateC.day:
                return True

        if delta is not None:
            dateB = dateB + delta

        if dateA.hour < dateB.hour:
            return True

        if dateA.hour == dateB.hour and dateA.minute <= dateB.minute:
            return True

        return False

    @staticmethod
    def get_check_only_year_months_day(dateA, dateB):
        if dateA.year < dateB.year:
            return True

        if dateA.year == dateB.year and dateA.month < dateB.month:
            return True

        if dateA.year == dateB.year and dateA.month == dateB.month and dateA.day <= dateB.day:
            return True

        return False

    @staticmethod
    def get_respondent_question(userid):
        logger.debug("Get respondent question")
        RespondentRepository = get_repository('RespondentRepository')
        QuestionRepository = get_repository('QuestionRepository')
        SurveyRepository = get_repository('SurveyRepository')
        AnswerRepository = get_repository('AnswerRepository')
        AnswerTextRepository = get_repository('AnswerTextRepository')
        RegistrationsRepository = get_repository('RegistrationsRepository')
        ResearchGroupRepository = get_repository('ResearchGroupRepository')

        repondent = RespondentRepository.get_by_id(userid)
        respondents = RegistrationsRepository.get_by_respondent_ids(repondent.ids)
        questions = []

        for respondent in respondents:
            research_group = ResearchGroupRepository.get_by_id(respondent.research_group_id)
            l = QuestionRepository.get_started_question_by_code(research_group.code)
            questions += l

        time_now = datetime.datetime.now()

        ans = []
        for question in questions:
            if question.status != 'deleted':
                survey = SurveyRepository.get_by_id(question.survey_id)
                if survey.startdate <= time_now <= survey.enddate:
                    timedelta = datetime.timedelta(seconds=survey.questiondelta)

                    for time in survey.times:
                        if Unit.get_check_only_minutes(time.time, time_now) and \
                                Unit.get_check_only_minutes(time_now, time.time, timedelta):
                            answers = AnswerRepository.get_by_question_id_and_user_id(question.id, userid)
                            f_a = True
                            for answer in answers:
                                if Unit.get_check_only_minutes(time.time, answer.date) and \
                                    Unit.get_check_only_minutes(answer.date, time.time, timedelta)\
                                        and \
                                    Unit.get_check_only_year_months_day(time_now, answer.date) and \
                                    Unit.get_check_only_year_months_day(answer.date, time_now + timedelta):
                                    f_a = False
                                    break

                            answers = AnswerTextRepository.get_by_question_id_and_user_id(question.id, userid)

                            if answers:
                                for answer in answers:
                                    if Unit.get_check_only_minutes(time.time, answer.date) and \
                                        Unit.get_check_only_minutes(answer.date, time.time,
                                                                    timedelta) and \
                                        Unit.get_check_only_year_months_day(time_now, answer.date) and \
                                        Unit.get_check_only_year_months_day(answer.date, time_now + timedelta):
                                        f_a = False
                                        break
                            if f_a:
                                ans.append(question)

        return ans

    def create_research_group(self, name, code=None, description=None):
        """
        Creates a new research group. The process of creating a new group requires a name.
        The name will be visible to participants of the study.
        Each research group is recognized by the participants of the study by means of a code.
        This code can be given manually, but it can also be generated randomly.

        Args:
            name (str): The name of new research group. This will be visible for participants
            code (str, optional): This code which will be use to join to research group by participants.
            description (str, optional): The description of research group. This will be visible for participants.

        Returns:
            New created research group

        Raises:
            None
        """
        ResearchGroupRepository = get_repository('ResearchGroupRepository')

        research_group = ResearchGroup(unit_id=self.id, code=code)

        research_group.name = name

        research_group.description=description
        research_group.user_id= self.user_id
        research_group.startdate = None
        research_group.enddate = None
        research_group.license = None
        research_group.ids = None
        ResearchGroupRepository.save(research_group)

        return research_group

