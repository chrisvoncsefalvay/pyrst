# coding=utf-8

class TokenException(Exception):
    """
    Raised when there is no token saved in the instance and a function that
    requires a token (i.e. any function other than login()) is called."
    """

    def __repr__(self):
        return "Cannot perform this operation without authentication token. Use" \
               " the login() method to obtain one."


class AuthException(Exception):
    """
    Raised when the user is not authorised.
    """

    def __repr__(self):
        return "Not authorised."


class ConnectionException(Exception):
    """
    Raised when the client could not connect for a network error.
    """

    def __repr__(self):
        return "Connection error."


class SpaceIDException(Exception):
    """
    Raised where a space ID is provided that does not meet the formal criteria
    for a space ID (36 characters separated by hyphens).
    """

    def __repr__(self):
        return "You have provided an incorrect space ID. A valid Birst space ID" \
               "is 36 characters long and consists of five groups of hexadecimal" \
               "characters separated by hyphens."


class MissingCredentialsException(AuthException):
    """
    Raised where an operation that requires credentials (e.g. login()) is
    called without providing the appropriate credentials, either directly
    or via a configuration file.
    """

    def __repr__(self):
        return "You need to provide a password and a username, either via your" \
               " configuration file or at the time of creating the Birst client " \
               "object."