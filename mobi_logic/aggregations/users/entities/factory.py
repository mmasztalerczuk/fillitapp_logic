import uuid
import logging

from taranis import publish
from taranis.abstract import Factory

from mobi_logic import get_repository
from mobi_logic.aggregations.users.entities.user import User
from mobi_logic.aggregations.users.exceptions import UserExists

logger = logging.getLogger(__name__)


# @TODO User abstract class for factory
class UserFactory(Factory):
    """User factory"""
    UserRepository = get_repository('UserRepository')

    @staticmethod
    def build(data):
        logger.debug("Building new user")

        event_id = str(uuid.uuid4())

        user = UserFactory.UserRepository.get_by_email(data['email'])

        # @TODO what about race condition during saving new user to db?
        if user:
            logger.info(f"Email already in db: {data['email']}")
            raise UserExists(data['email'])

        event = User.Created(id=event_id,
                             email=data['email'],
                             password=data['password'])

        logger.debug(f"Publishing new user for email: {data['email']}")
        publish(event)
