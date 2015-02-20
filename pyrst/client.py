from base64 import b64decode

from suds.client import Client
import yaml

from pyrst.exceptions import SpaceIDException, MissingCredentialsException, MissingInstanceException
from pyrst.decorators import check_token
from pyrst.handlers import *
from pyrst.helpers import Instance, instance_helper


class BirstClient(object):
    """
    Basic Birst client object.
    """

    def __init__(self,
                 user=None,
                 password=None,
                 instance="app2102",
                 configfile=None):

        if configfile:
            with open(configfile, 'r') as _c:
                _config_dict = yaml.load(_c)

            self.password = _config_dict["password"]
            self.user = _config_dict["username"]
            instance = _config_dict["instance"]

            if _config_dict["password_is_encrypted"] is True:
                self.password = b64decode(_config_dict["password"])
            else:
                self.password = _config_dict["password"]

        else:
            self.user = user
            self.password = password

        if not self.password or not self.user:
            raise MissingCredentialsException

        if not instance:
            raise MissingInstanceException

        self.instance = "https://" + instance + ".bws.birst.com/CommandWebService.asmx?wsdl"
        self.token = None

        self.connector = Client(self.instance, location=self.instance)

    def __repr__(self):
        return "Birst client instance for user %s at %s" % (self.user, self.instance)


    ####################
    # LOGIN AND LOGOUT #
    ####################
    #
    # The login API exposes two (fairly selfexplanatory) methods:
    # - login
    # - logout
    #
    # There is no manual token handling in Pyrst - upon login, your token will
    # be appended to the instance as an instance variable.

    # login

    def login(self):
        """
        Logs the user in to the instance specified in the basic settings of the
        class with the password and username specified.
        If successful, the token returned will be appended to the class instance
        as an instance variable.
        """

        try:
            self.token = self.connector.service.Login(self.user, self.password)
            print "You have been successfully logged in, %s." % self.user
            print "Your token is: %s" % self.token
        except Exception as e:
            return e

    # logout

    @check_token
    def logout(self):
        """
        Logs the user out and deletes the token saved in the instance.
        """
        try:
            self.connector.service.Logout(self.token)
            self.token = None
            print "You have been logged out."
        except Exception as e:
            return e

    ############
    # QUERYING #
    ############
    #
    # The query interface exposes three methods:
    # - executequery: simple querying
    # - more: continue querying
    # - retrieve: keep querying as long as there are results.
    #
    # Unlike in Birst's XML API, in Pyrst, the space comes _before_ the query -
    # this is much more intuitive since the query is subordinate to the space
    # rather than the other way around.

    # executequery

    # TODO: Handlerise this!

    @check_token
    def executequery(self,
                     space,
                     query,
                     handler=None):
        """
        Retrieves the first 1,000 results for the query.

        :param space: SpaceID of the space (incl. hyphens, 36 chars)
        :param query: Birst BQL query
        :param handler: instance of output handler class
        :return: query result
        """
        if len(space) != 36:
            raise SpaceIDException
        else:
            result = self.connector.service.executeQueryInSpace(self.token,
                                                                query,
                                                                space)

        if handler:
            _handler = handler()
            return _handler.process(result)
        else:
            return result

    # retrieve

    @check_token
    def retrieve(self,
                 space,
                 query,
                 handler=None):
        """
        Retrieves the entire dataset for the query.

        :param space: SpaceID of the space (incl. hyphens, 36 chars)
        :param query: Birst BQL query
        :param handler: instance of output handler class
        :return: query result
        """

        if len(space) != 36:
            raise SpaceIDException
        else:

            result = self.connector.service.executeQueryInSpace(self.token,
                                                                query,
                                                                space)
            r = instance_helper(result)
            has_more_rows = result.hasMoreRows
            query_token = result.queryToken

            while has_more_rows is True:
                m = self.connector.service.queryMore(self.token,
                                                     query_token)
                r.rows += m.rows[0]
                has_more_rows = m.hasMoreRows

        if handler:
            _handler = handler()
            return _handler.process(r)
        else:
            return r
