import uuid
from datetime import timedelta, datetime

from taranis.abstract import DomainEvent

from mobi_logic import get_repository
from mobi_logic.aggregations.organization.domain.entities.question import Question
from mobi_logic.aggregations.organization.domain.entities.survey_time import SurveyTime
from mobi_logic.aggregations.organization.exceptions.errors import QuestionNotFound


class Survey:

    class STATUS:
        NEW = 'new'
        DELETED = 'deleted'
        STARTED = 'started'

    @property
    def survey_repository(self):
        return get_repository('QuestionRepository')

    class Created(DomainEvent):
        type = "Survey.Created"

    def create_question(self, name, type):
        QuestionRepository = get_repository('QuestionRepository')

        question = Question()

        question.id=str(uuid.uuid4())
        question.ids = None
        question.survey_id = self.id
        question.unit_id = self.unit_id
        question.name=name
        question.type = type
        question.status = Question.STATUS.NEW

        QuestionRepository.save(question)

        return question

    def add_time(self, time):
        SurveyTimeRepository = get_repository('SurveyTimeRepository')
        surveyTime = SurveyTime()
        surveyTime.id = str(uuid.uuid4())
        surveyTime.time = time
        surveyTime.survey_id = self.id

        SurveyTimeRepository.save(surveyTime)

    def get_question(self, question_id, deleted=False):
        for question in self.questions:
            if question.id == question_id:
                if not deleted and question.status != Question.STATUS.DELETED:
                    return question
                raise QuestionNotFound
        raise QuestionNotFound

    def remove_question(self, question_id):
        for question in self.questions:
            if question.id == question_id:
                question.status = Question.STATUS.DELETED
                self.survey_repository.save(question)
                break

        # @TODO throw exception on missing survey

    def get_responses(self, code):
        ResearchGroupRepository = get_repository('ResearchGroupRepository')
        RegistrationsRepository = get_repository('RegistrationsRepository')
        ResponseRepository = get_repository('ResponseRepository')
        RespondentRepository = get_repository('RespondentRepository')
        SurveyRepository = get_repository('SurveyRepository')

        t = self.startdate
        one_day = timedelta(days=1)
        l = []

        research_group = ResearchGroupRepository.get_by_code(code)
        registrations = RegistrationsRepository.get_by_research_group_id(research_group.id)

        for registration in registrations:
            respondent = RespondentRepository.get_by_ids(registration.respondent_ids)

            t = self.startdate

            while t < self.enddate:
                for time in self.times:
                    start_date = datetime(year=t.year, month=t.month, day=t.day, hour=time.time.hour, minute=time.time.minute)
                    d = {'date': start_date, 'user-id': respondent.id}
                    for question in self.questions:
                        for answer in question.answers:
                            if start_date <= answer.date < start_date + timedelta(
                                    seconds=self.questiondelta) and answer.user_id == respondent.id:
                                if question.id in d:
                                    d[question.id] += ":" + ResponseRepository.get_by_id(answer.response_id).value
                                else:
                                    d[question.id] = ResponseRepository.get_by_id(answer.response_id).value
                        for answer in question.answers_text:
                            if start_date <= answer.date < start_date + timedelta(
                                    seconds=self.questiondelta) and answer.user_id == respondent.id:
                                d[question.id] = answer.text


                    l.append(d)
                t += one_day

        return l


    def update_values(self, data):
        SurveyRepository = get_repository('SurveyRepository')

        if data.get('status') and data['status'] == Survey.STATUS.STARTED:
            self.status = data['status']

        if data.get('startdate'):
            self.startdate = datetime(year=data.get('startdate').year, month=data.get('startdate').month, day=data.get('startdate').day)

        if data.get('enddate'):
            self.enddate = datetime(year=data.get('enddate').year, month=data.get('enddate').month, day=data.get('enddate').day) + \
                           timedelta(hours=23, minutes=59)

        if data.get('description'):
            self.description = data['description']

        if data.get('name'):
            self.name = data['name']

        if data.get('questiondelta'):
            self.questiondelta = data['questiondelta']

        SurveyRepository.save(self)
