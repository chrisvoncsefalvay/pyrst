class Instance(object):

    def __init__(self,
                 colnames,
                 rows):
        self.colnames = colnames
        self.rows = rows


def instance_helper(instance):

    column_names = instance.columnNames[0]
    rows = instance.rows[0]

    i = Instance(colnames=column_names,
                 rows=rows)

    return i