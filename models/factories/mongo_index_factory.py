from pymongo import IndexModel


class MongoIndexFactory:
    def create(self, columns) -> list:
        return [
            IndexModel([(column.name, column.sorting_order)], background=True, name=column.name)
            for column in columns
        ]


class MongoColumnFactory:
    def ascending(self, column_name):
        return MongoColumn(column_name, 1)

    def descending(self, column_name):
        return MongoColumn(column_name, -1)


class MongoColumn:
    def __init__(self, name, sorting_order):
        self.name = name
        self.sorting_order = sorting_order
