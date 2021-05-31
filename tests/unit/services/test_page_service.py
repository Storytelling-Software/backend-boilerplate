import pytest

from mock import Mock
from services import PageService
from handlers.base_handler import Paging
from infrastructure.exceptions import InvalidRequestException


class TestPageService:
    def setup(self):
        self.service = PageService()
        self.repository_mock = Mock()

    def test_get_page_with_valid_params(self):
        paging = Paging()
        paging.page = 3
        paging.page_size = 10

        self.repository_mock.get_page.return_value = [Mock(), Mock()]
        self.repository_mock.count.return_value = 32

        page = self.service.get_page(
            paging, self.repository_mock.get_page, self.repository_mock.count)

        assert page.page == 3
        assert page.page_count == 4
        self.repository_mock.count.assert_called_once()
        self.repository_mock.get_page.assert_called_once_with(20, 10)

    def test_invalid_paging(self):
        paging = Paging()
        paging.page = -1
        paging.page_size = -1

        with pytest.raises(InvalidRequestException) as ex:
            self.service.get_page(
                paging, self.repository_mock.get_page, self.repository_mock.count
            )

        assert ex.value.errors == {
            'page': ['should be greater than zero'],
            'page_size': ['should be greater than zero']
        }

    def test_get_page_0(self):
        paging = Paging()
        paging.page = 1
        paging.page_size = 10

        self.repository_mock.get_page.return_value = []
        self.repository_mock.count.return_value = 0

        page = self.service.get_page(
            paging, self.repository_mock.get_page, self.repository_mock.count)

        assert page.page == 1
        assert page.page_count == 1
        self.repository_mock.count.assert_called_once()
        self.repository_mock.get_page.assert_called_once_with(0, 10)
