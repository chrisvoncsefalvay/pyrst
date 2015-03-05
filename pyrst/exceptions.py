# coding=utf-8

import logging
module_logger = logging.getLogger("pyrst.client")
module_logger.setLevel(logging.DEBUG)


class PyrstException(Exception):
    """
    Generic, abstract class of exception.
    """

    def __init__(self):
        self.logger = logging.getLogger("pyrst.client")
        self.logger.warning(self.__repr__())


class TokenException(PyrstException):
    """
    Raised when there is no token saved in the instance and a function that
    requires a token (i.e. any function other than login()) is called."
    """

    def __repr__(self):
        return "Cannot perform this operation without authentication token. Use" \
               " the login() method to obtain one."


class AuthException(PyrstException):
    """
    Raised when the user is not authorised.
    """

    def __repr__(self):
        return "Not authorised."


class ConnectionException(PyrstException):
    """
    Raised when the client could not connect for a network error.
    """

    def __repr__(self):
        return "Connection error."


class SpaceIDException(PyrstException):
    """
    Raised where a space ID is provided that does not meet the formal criteria
    for a space ID (36 characters separated by hyphens).
    """

    def __repr__(self):
        return "You have provided an incorrect space ID. A valid Birst space ID" \
               "is 36 characters long and consists of five groups of hexadecimal" \
               "characters separated by hyphens."


class MissingCredentialsException(PyrstException):
    """
    Raised where an operation that requires credentials (e.g. login()) is
    called without providing the appropriate credentials, either directly
    or via a configuration file.
    """

    def __repr__(self):
        return "You need to provide a password and a username, either via your" \
               " configuration file or at the time of creating the Birst client " \
               "object."