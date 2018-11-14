from abc import ABCMeta


class UserRepositoryAbstract(metaclass=ABCMeta):

    def get_by_email(self, email):
        raise NotImplemented
