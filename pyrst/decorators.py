# coding=utf-8
from exceptions import TokenException


def check_token(func):
    """
    Checks whether the instance variable on the object from which the function
    `func` is called has its internals set.

    :param func: function
    :return: function
    :raise: TokenException if no token is saved in the instance.
    """

    def inner(self, *args, **kwargs):
        if self.token is None:
            raise TokenException
        else:
            return func(self, *args, **kwargs)
    return inner
