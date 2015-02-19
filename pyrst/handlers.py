import pandas as pd

class Handler(object):

    def __repr__(self):
        return "Pyrst output handler: %s" % self.name

    def process(self,
                query_output):
        return query_output


class DfHandler(Handler):
    """
    Handler that returns a Pandas dataFrame
    """

    def process(self,
                query_output):

        _series = []
        for each in query_output.rows[0]:
            _series.append(pd.Series(each[0]))

        _df = pd.DataFrame(_series)

        _colnames = []
        for each in query_output.columnNames[0]:
            _colnames.append(str(each))

        _df.columns = _colnames

        return _df
