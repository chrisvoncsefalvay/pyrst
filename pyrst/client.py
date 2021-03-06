# coding=utf-8

from suds.client import Client

from base64 import b64decode
import yaml
import types
import logging

from pyrst.exceptions import SpaceIDException, MissingCredentialsException
from pyrst.decorators import check_token
from pyrst.handlers import Handler, JsonHandler, DfHandler, CsvHandler

module_logger = logging.getLogger("pyrst.client")
module_logger.setLevel(logging.ERROR)
default_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
module_handler = logging.StreamHandler()
module_logger.addHandler(module_handler)


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

        self.logger = module_logger
        self.logger.info("Creating Birst connector...")

        if configfile:
            self.logger.info("Using configuration file {configfile}".format(configfile=configfile))
            with open(configfile) as _c:
                _config_dict = yaml.load(_c)

            self.password = _config_dict["password"]
            self.user = _config_dict["username"]
            instance = _config_dict["instance"]

            self.logger.debug("User: {username} on instance {instancename}".
                              format(username=self.user,
                                     instancename=instance))

            if _config_dict["password_is_encrypted"] is True:
                self.password = b64decode(_config_dict["password"])
            else:
                self.password = _config_dict["password"]

        else:
            self.user = user
            self.password = b64decode(password)

        if not self.password or not self.user:
            raise MissingCredentialsException

        self.instance = "https://{instancename}.bws.birst.com/CommandWebService.asmx?wsdl"\
            .format(instancename=instance)
        self.token = None

        self.connector = Client(self.instance, location=self.instance)
        self.logger.debug("Connector set up successfully.")

    def __repr__(self):
        return "Birst client instance for user {username} at {instance}".format(username=self.user,
                                                                                instance=self.instance)

    ####################
    # LOGIN AND LOGOUT #
    ####################
    #
    # The login API exposes two (fairly self-explanatory) methods:
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
            self.logger.info("You have been successfully logged in, {username}.\n"
                             "Your token is: {token}".format(username=self.user,
                                                             token=self.token))
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
            self.logger.info("Logging out {user}...".format(user=self.user))
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

        result = [{"name": each["name"],
                   "owner": each["owner"],
                   "id": each["id"]} for each in p]

        self.logger.info("{spaces} spaces found, listing.".format(spaces = len(result)))
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
            self.logger.debug("Query:\n{querystring}".format(querystring=query))
            self.logger.debug("Space: {spaceid}".format(spaceid=space))
            self.logger.debug("Handled by {handler_class}."
                              .format(handler_class=handler.__name__ if handler else "raw output"))

            result = self.connector.service.executeQueryInSpace(self.token,
                                                                query,
                                                                space)

        if handler:
            self.logger.debug("Submitting rows to handler {handler_class_name}."
                              .format(handler.__class__.__name__))
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
            self.logger.debug("Query:\n{querystring}".format(querystring=query))
            self.logger.debug("Space: {spaceid}".format(spaceid=space))
            self.logger.debug("Handled by {handler_class}."
                              .format(handler_class=handler.__name__ if handler else "raw output"))

            result = self.connector.service.executeQueryInSpace(self.token,
                                                                query,
                                                                space)

            _result_struct = {"columnNames": result.columnNames[0],
                              "rows": result.rows[0],
                              "dataTypes": result.dataTypes[0],
                              "hasMoreRows": result.hasMoreRows}

            while _result_struct['hasMoreRows']:
                _result_struct["queryToken"] = result.queryToken
                _more_query = self.connector.service.queryMore(self.token,
                                                               _result_struct['queryToken'])
                _result_struct["rows"] += _more_query["rows"][0]
                _result_struct["hasMoreRows"] = _more_query["hasMoreRows"]

        if handler:
            self.logger.debug("Submitting rows to handler {handlerclass}.".format(handlerclass=handler))
            if isinstance(handler, types.TypeType):
                _handler = handler()
                return _handler.process(_result_struct)
            else:
                return handler.process(_result_struct)
        else:
            return _result_struct
