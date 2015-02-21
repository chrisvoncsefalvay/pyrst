# coding=utf-8

class ResultSet(object):
    """
    A wrapper for returned result sets.
    """

    def __init__(self,
                 colnames,
                 rows):
        self.colnames = colnames
        self.rows = rows


def result_set_helper(query_results):
    """
    Wraps returned data into convenient objects (ResultSets) that encapsulate
    the rows returned and the column names. These can then be fed to Handlers.

    :param query_results: query results from Birst, a complex object
    :type query_results: instance
    :return: a ResultSet object representing the result set of the query
    :rtype: ResultSet
    """

    column_names = query_results.columnNames[0]
    rows = query_results.rows[0]

    i = ResultSet(colnames=column_names,
                 rows=rows)

    return i