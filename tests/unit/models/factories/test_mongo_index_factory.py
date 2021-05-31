from models.factories.mongo_index_factory import MongoIndexFactory, MongoColumnFactory, MongoColumn

from mock import Mock
from pymongo import IndexModel


class TestIndexFactory:
    def setup(self):
        self.factory = MongoIndexFactory()
        self.column_mock = Mock()

    def test_create(self):
        self.column_mock.name = 'mock_name'
        self.column_mock.sorting_order = 1

        result = self.factory.create(
            [self.column_mock]
        )

        assert isinstance(result, list) is True
        assert len(result) == 1
        assert isinstance(result[0], IndexModel) is True
        index_document = result[0].document

        assert index_document['background'] is True
        assert index_document['name'] == 'mock_name'
        assert 'mock_name' in index_document.get('key').items()[0]
        assert 1 in index_document.get('key').items()[0]


class TestMongoColumnFactory:
    def setup(self):
        self.factory = MongoColumnFactory()

    def test_ascending(self):
        column_name = 'user_id'
        result = self.factory.ascending(column_name)

        assert isinstance(result, MongoColumn) is True
        assert result.name == column_name
        assert result.sorting_order == 1

    def test_descending(self):
        column_name = 'user_id'
        result = self.factory.descending(column_name)

        assert isinstance(result, MongoColumn) is True
        assert result.name == column_name
        assert result.sorting_order == -1
