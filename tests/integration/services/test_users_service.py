from models import User
from mock import Mock

from structure import structure

from models.page import Page
from handlers.base_handler import Paging
from ...factories.user import UserFactory


class TestUsersService:
    def setup(self):
        self.service = structure.instantiate('users_service')
        self.repository = structure.instantiate('users_repository')

        self.page_service = structure.instantiate('page_service')
        self.service.user_email_service = Mock()
        self.factory = UserFactory()

    def teardown(self):
        self.repository.collection.delete_many({})

    def test_get_page(self):
        first_user = self.factory.generic('user')
        first_user.id = self.repository.create(first_user)

        second_user = self.factory.generic('user')
        second_user.id = self.repository.create(second_user)

        third_user = self.factory.generic('user')
        third_user.id = self.repository.create(third_user)

        paging = Paging()
        paging.page = 1
        paging.page_size = 10

        result = self.service.get_page(paging, 'user')

        assert isinstance(result, Page) is True
        assert isinstance(result.items, list) is True
        assert len(result.items) == 3

        assert isinstance(result.items[0], User) is True
        assert result.items[0].id == third_user.id
        assert result.items[0].email == third_user.email
        assert result.items[0].role == third_user.role
        assert result.items[0].password_hash == third_user.password_hash
        assert result.items[0].token_pairs == third_user.token_pairs
        assert result.items[0].profile.first_name == third_user.profile.first_name
        assert result.items[0].profile.last_name == third_user.profile.last_name

        assert isinstance(result.items[1], User) is True
        assert result.items[1].id == second_user.id
        assert result.items[1].email == second_user.email
        assert result.items[1].role == second_user.role
        assert result.items[1].password_hash == second_user.password_hash
        assert result.items[1].token_pairs == second_user.token_pairs
        assert result.items[1].profile.first_name == second_user.profile.first_name
        assert result.items[1].profile.last_name == second_user.profile.last_name

    def test_search_by_query_email(self):
        first_user = self.factory.generic('user')
        first_user.id = self.repository.create(first_user)

        second_user = self.factory.generic('user')
        second_user.id = self.repository.create(second_user)

        third_user = self.factory.generic('user')
        third_user.id = self.repository.create(third_user)

        query = first_user.email
        role = first_user.role

        paging = Paging()
        paging.page = 1
        paging.page_size = 10

        result = self.service.search(paging, query, role)

        assert isinstance(result, Page) is True
        assert isinstance(result.items, list) is True
        assert len(result.items) == 1

        assert isinstance(result.items[0], User) is True
        assert result.items[0].id == first_user.id
        assert result.items[0].email == first_user.email
        assert result.items[0].role == first_user.role
        assert result.items[0].password_hash == first_user.password_hash
        assert result.items[0].token_pairs == first_user.token_pairs
        assert result.items[0].profile.first_name == first_user.profile.first_name
        assert result.items[0].profile.last_name == first_user.profile.last_name

    def test_search_by_query_name(self):
        first_user = self.factory.generic('user')
        first_user.id = self.repository.create(first_user)

        second_user = self.factory.generic('user')
        second_user.id = self.repository.create(second_user)

        third_user = self.factory.generic('user')
        third_user.id = self.repository.create(third_user)

        query = third_user.profile.first_name + ' ' + third_user.profile.last_name
        role = third_user.role

        paging = Paging()
        paging.page = 1
        paging.page_size = 10

        result = self.service.search(paging, query, role)

        assert isinstance(result, Page) is True
        assert isinstance(result.items, list) is True
        assert len(result.items) == 1

        assert isinstance(result.items[0], User) is True
        assert result.items[0].id == third_user.id
        assert result.items[0].email == third_user.email
        assert result.items[0].role == third_user.role
        assert result.items[0].password_hash == third_user.password_hash
        assert result.items[0].token_pairs == third_user.token_pairs
        assert result.items[0].profile.first_name == third_user.profile.first_name
        assert result.items[0].profile.last_name == third_user.profile.last_name

    def test_search_by_query_not_existing_name(self):
        first_user = self.factory.generic('user')
        first_user.profile.first_name = 'John'
        first_user.profile.last_name = 'Doe'
        first_user.id = self.repository.create(first_user)

        query = 'ane Doe'
        role = first_user.role

        paging = Paging()
        paging.page = 1
        paging.page_size = 10

        result = self.service.search(paging, query, role)

        assert isinstance(result, Page) is True
        assert isinstance(result.items, list) is True
        assert len(result.items) == 0
