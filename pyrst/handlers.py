# coding=utf-8

import pandas as pd


class Handler(object):
    """
    Abstract class that represents Handler objects.

    In Pyrst, a Handler object receives the raw query result and converts it
    into a specified format, such as a pandas DataFrame or a D3 compatible
    JSON file.

    A Handler needs to have a process() function that takes the query_output
    as its argument. The return of that function is going to be the output of
    the Handler.
    """

    def __repr__(self):
        return "Pyrst output handler: %s" % self.name

    def process(self,
                query_output):
        return query_output


class DfHandler(Handler):
    """
    Handler that returns a Pandas dataFrame.
    """

    def process(self,
                query_output):

        _series = []
        for each in query_output.rows:
            _series.append(each[0])

        _df = pd.DataFrame(_series)

        _df.columns = query_output.colnames

        return _df


class JsonHandler(Handler):
    """
    Handler that returns a JSON file, ready to be ingested by D3.

    Currently, this is implemented 'lazily', i.e. the DfHandler is invoked,
    and the output is then exported into JSON using pandas's JSON export
    function. Eventually, we will aim to create a thoroughbred JSON export
    function.
    """

    def __init__(self,
                 orient="records",
                 date_format="iso"):
        self.orient = orient
        self.date_format = date_format

    def process(self,
                query_output):

        _series = []
        for each in query_output.rows:
            _series.append(each[0])

        _df = pd.DataFrame(_series)

        _df.columns = query_output.colnames

        return _df.to_json(orient=self.orient,
                           date_format=self.date_format)


class CsvHandler(Handler):
    """
    Handler that returns a CSV file, ready to be ingested by Excel etc..

    Currently, this is implemented 'lazily', i.e. the DfHandler is invoked,
    and the output is then exported into JSON using pandas's CSV export
    function. Eventually, we will aim to create a thoroughbred CSV export
    function.
    """

    def __init__(self,
                 sep=',',
                 encoding="utf-8",
                 index=False):
        self.sep = sep
        self.encoding = encoding
        self.index = index

    def process(self,
                query_output):

        _series = []
        for each in query_output.rows:
            _series.append(each[0])

        _df = pd.DataFrame(_series)

        _df.columns = query_output.colnames

        return _df.to_csv(sep=self.sep,
                          encoding=self.encoding,
                          index=self.index)
