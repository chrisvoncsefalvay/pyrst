# coding=utf-8

from base64 import b64decode

from suds.client import Client
import yaml
import types
import logging

from pyrst.exceptions import SpaceIDException, MissingCredentialsException
from pyrst.decorators import check_token
from pyrst.handlers import Handler
from pyrst.helpers import ResultSet, result_set_helper

module_logger = logging.getLogger("pyrst.client")
module_logger.setLevel(logging.DEBUG)

class BirstClient(object):
    """
    Basic Birst client object.
    """

    def __init__(self,
                 user=None,
                 password=None,
                 instance="app2102",
                 configfile=None):
        """
        Creates the Birst client object.

        Birst client objects can be created either by directly supplying the
        username and the base64-encoded password or by putting it in a
        separate configuration file. The latter version is much preferred,
        as that way, the password will not be present in your code, not even
        in a generally non-trivially readable form. It's important to ensure
        that other than the Python process using Pyrst, no other processes or
        users have access to the configuration file.

        :param user: username
        :type user: str
        :param password: password, encrypted in base64
        :type password: str
        :param instance: name of the instance (e.g. 'app2102'). Defaults to
        app2102.
        :type instance: str
        :param configfile: relative path to a configuration file.
        :type configfile: str
        """

        self.logger = logging.getLogger("pyrst.client")
        self.logger.info("Creating Birst connector...")

        if configfile:
            self.logger.info("Using configuration file %s" % configfile)
            with open(configfile) as _c:
                _config_dict = yaml.load(_c)

            self.password = _config_dict["password"]
            self.user = _config_dict["username"]
            instance = _config_dict["instance"]

            self.logger.debug("User: %s on instance %s" % (self.user, instance))


            if _config_dict["password_is_encrypted"] is True:
                self.password = b64decode(_config_dict["password"])
            else:
                self.password = _config_dict["password"]

        else:
            self.user = user
            self.password = b64decode(password)

        if not self.password or not self.user:
            raise MissingCredentialsException

        self.instance = "https://" + instance + ".bws.birst.com/CommandWebService.asmx?wsdl"
        self.token = None

        self.connector = Client(self.instance, location=self.instance)
        self.logger.debug("Connector set up successfully.")

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

        :return: token
        :rtype: str
        """

        try:
            self.logger.debug("Obtaining token now...")
            self.token = self.connector.service.Login(self.user, self.password)
            self.logger.info("You have been successfully logged in, %s." % self.user)
            self.logger.info("Your token is: %s" % self.token)
            return self.token
        except Exception as e:
            return e

    # logout

    @check_token
    def logout(self):
        """
        Logs the user out and deletes the token saved in the instance.
        """
        try:
            self.logger.info("Logging out %s..." % self.user)
            self.connector.service.Logout(self.token)
            self.token = None
            self.logger.warn("You have been logged out.")
        except Exception as e:
            return e


    ##################
    # LISTING SPACES #
    ##################
    #
    # Listing spaces the user has access to.

    # listspaces

    @check_token
    def listspaces(self):
        """
        Lists spaces.

        :return: array of dicts, each representing a space.
        :type: list of dict of (str, str, str)
        """
        self.logger.debug("Listing spaces available to user %s..." % self.user)
        p = self.connector.service.listSpaces(self.token).UserSpace

        result = []
        for each in p:
            result.append({"name": each["name"],
                           "owner": each["owner"],
                           "id": each["id"]})
        self.logger.info("%i spaces found, listing." % len(result))
        return result


    ############
    # QUERYING #
    ############
    #
    # The query interface exposes two methods:
    # - executequery: simple querying
    # - retrieve: keep querying as long as there are results.
    #
    # Unlike in Birst's XML API, in Pyrst, the space comes _before_ the query -
    # this is much more intuitive since the query is subordinate to the space
    # rather than the other way around.

    # executequery

    @check_token
    def executequery(self,
                     space,
                     query,
                     handler=None):
        """
        Retrieves the first 1,000 results for the query.

        :param space: SpaceID of the space (incl. hyphens, 36 chars)
        :type space: str
        :param query: Birst BQL query
        :type query: str
        :param handler: output handler class or output handler class instance
        :type handler: Handler
        :return: query result as processed by the handler
        """
        if len(space) != 36:
            raise SpaceIDException
        else:
            self.logger.debug("Executing query.")
            self.logger.debug("Query:\n%s" % query)
            self.logger.debug("Space: %s" % space)
            self.logger.debug("Handled by: %s" % (handler if handler else "raw output"))

            result = self.connector.service.executeQueryInSpace(self.token,
                                                           query,
                                                           space)

        if handler:
            self.logger.debug("Submitting rows to handler %s." % handler)
            if type(handler) is ResultSet:
                return handler.process(result)
            else:
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
        Retrieves the entire dataset for the query, repeating the `queryMore`
        command as long as there are results. Please be aware that for large
        queries, *this may take some time*.

        :param space: SpaceID of the space (incl. hyphens, 36 chars)
        :type space: str
        :param query: Birst BQL query
        :type query: str
        :param handler: output handler class or output handler class instance
        :type handler: Handler
        :return: query result as processed by the query handler.
        """

        if len(space) != 36:
            raise SpaceIDException
        else:
            self.logger.debug("Executing query.")
            self.logger.debug("Query:\n%s" % query)
            self.logger.debug("Space: %s" % space)
            self.logger.debug("Handled by: %s" % (handler if handler else "raw output"))

            result = self.connector.service.executeQueryInSpace(self.token,
                                                                query,
                                                                space)

            r = result_set_helper(result)
            has_more_rows = result.hasMoreRows
            self.logger.debug("First result set received.")
            query_token = result.queryToken
            self.logger.debug("Query token: %s" % query_token)

            while has_more_rows is True:
                m = self.connector.service.queryMore(self.token,
                                                     query_token)
                self.logger.debug("Receiving batch of %i rows." % (m.numRowsReturned))
                r.rows += m.rows[0]
                has_more_rows = m.hasMoreRows
            self.logger.debug("Completed receiving rows. %i rows received." % len(r.rows))

        if handler:
            self.logger.debug("Submitting rows to handler %s." % handler)
            if isinstance(handler, types.TypeType):
                _handler = handler()
                return _handler.process(r)
            else:
                return handler.process(r)
        else:
            return r