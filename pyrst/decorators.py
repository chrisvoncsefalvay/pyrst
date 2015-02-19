# from exceptions import TokenException


def check_token(func):
    """
    Checks whether the instance variable on the object from which the function
    `func` is called has its internals set.

    :param func:
    :return:
    """

    def inner(self, *args, **kwargs):
        if self.token is None:
            raise NameError
        else:
            return func(self, *args, **kwargs)
    return inner
