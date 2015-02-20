# coding=utf-8

class TokenException(Exception):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Cannot perform operation without authentication token. Use the" \
               "Login() function to obtain one."


class AuthException(Exception):

    def __repr__(self):
        return "Not authorised."


class ConnectionException(Exception):

    def __repr__(self):
        return "Connection error."


class SpaceIDException(Exception):

    def __repr__(self):
        return "You have provided an incorrect space ID. A valid Birst space ID" \
               "is 36 characters long and consists of five groups of hexadecimal" \
               "characters separated by hyphens."


class MissingCredentialsException(AuthException):

    def __repr__(self):
        return "You need to provide a password and a username, either via your" \
               " configuration file or at the time of creating the Birst client " \
               "object."


class MissingInstanceException(AuthException):

    def __repr__(self):
        return "You need to provide a Birst instance name, either via your" \
               " configuration file or at the time of creating the Birst client " \
               "object."