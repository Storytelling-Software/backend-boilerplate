import pytest

from services import UsersService
from mock import Mock
from faker import Faker
from bson import ObjectId

from ...factories import UserFactory
from models import Page, User, UserApplication
from infrastructure.exceptions import NotFoundException


class TestUsersService:
    def setup(self):
        self.users_repository = Mock()
        self.user_applications_repository = Mock()
        self.password_service = Mock()
        self.create_request_validator_service = Mock()
        self.create_admin_validator_service = Mock()
        self.update_request_validator_service = Mock()
        self.create_cashout_validator_service = Mock()
        self.page_service = Mock()
        self.email_list_service = Mock()
        self.user_email_service = Mock()
        self.user_files_migration_service = Mock()
        self.service = UsersService(
            self.users_repository,
            self.user_applications_repository,
            self.password_service,
            self.create_request_validator_service,
            self.create_admin_validator_service,
            self.update_request_validator_service,
            self.page_service,
            self.email_list_service,
            self.user_email_service,
            self.user_files_migration_service
        )
        self.faker = Faker()
        self.factory = UserFactory()

        assert self.service.users_repository == self.users_repository
        assert self.service.password_service == self.password_service
        assert self.service.create_user_validator_service == self.create_request_validator_service
        assert self.service.create_admin_validator_service == self.create_admin_validator_service
        assert self.service.update_user_validator_service == self.update_request_validator_service
        assert self.service.page_service == self.page_service
        assert self.service.email_list_service == self.email_list_service
        assert self.service.user_email_service == self.user_email_service

    def test_confirmed_user_is_added_to_mailchimp(self):
        application = UserApplication.from_request({
            'email': self.faker.email(),
            'password_hash': '',
            'role': 'user',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        })
        self.user_applications_repository.find_by_email.return_value = application
        attributes = {
            'email': application.email,
            'code': application.code
        }

        user = self.service.confirm_registration(attributes)
        self.email_list_service.add_user.assert_called_once()
        assert user.created_at is not None

    def test_create_admin_successful(self):
        email = self.faker.email()
        attributes = {
            'email': email,
            'profile': {
                'first_name': 'John',
                'last_name': 'Doe'
            }
        }
        user_id = ObjectId()
        self.users_repository.create.return_value = user_id
        self.password_service.generate_password.return_value = 'test_password'

        admin = self.service.create_admin(attributes)

        self.create_admin_validator_service.validate.assert_called_once_with(attributes)
        self.password_service.generate_password.assert_called_once_with(8)
        self.password_service.create_hash.assert_called_once()
        self.users_repository.create.assert_called_once()

        self.user_email_service.send_account_details.assert_called_once_with(admin, 'test_password')

        assert admin.id == user_id
        assert admin.role == 'admin'
        assert admin.email == email
        assert admin.profile.first_name == 'John'
        assert admin.profile.last_name == 'Doe'
        assert admin.created_at is not None

    def test_create_admin_unsuccessful(self):
        email = self.faker.email()
        attributes = {
            'email': email,
            'profile': {
                'first_name': 'John',
                'last_name': 'Doe'
            }
        }

        self.users_repository.create.return_value = None
        self.password_service.generate_password.return_value = 'test_password'

        self.service.create_admin(attributes)

        self.create_admin_validator_service.validate.assert_called_once_with(attributes)
        self.password_service.generate_password.assert_called_once_with(8)
        self.password_service.create_hash.assert_called_once()
        self.users_repository.create.assert_called_once()

        self.user_email_service.send_account_details.assert_not_called()

    def test_create_user_no_password(self):
        attributes = {
            'email': self.faker.email(),
            'profile': {
                'first_name': 'John',
                'last_name': 'Doe',
            }
        }
        self.user_applications_repository.find_by_email.return_value = None
        self.service.create(attributes)

        self.create_request_validator_service.validate.assert_called_once_with(attributes)
        self.password_service.generate_password.assert_called_once_with(8)
        self.user_applications_repository.create.assert_called_once()
        self.user_email_service.send_account_confirmation.assert_called_once()

    def test_create_user_with_password(self):
        attributes = {
            'email': self.faker.email(),
            'password': 'test_password',
            'profile': {
                'first_name': 'John',
                'last_name': 'Doe',
            }
        }
        self.user_applications_repository.find_by_email.return_value = None
        self.service.create(attributes)

        self.create_request_validator_service.validate.assert_called_once_with(attributes)
        self.password_service.generate_password.assert_not_called()
        self.user_applications_repository.create.assert_called_once()
        self.user_email_service.send_account_confirmation.assert_called_once()

    def test_find_missing_user(self):
        user_id = ObjectId()
        self.users_repository.find_by_id.return_value = None

        with pytest.raises(NotFoundException):
            self.service.find(user_id)

        self.users_repository.find_by_id.assert_called_once_with(user_id)

    def test_find_existing_user(self):
        user = self.factory.generic('user')
        user.id = ObjectId()
        self.users_repository.find_by_id.return_value = user
        result = self.service.find(user.id)

        self.users_repository.find_by_id.assert_called_once_with(user.id)

        assert result.id == user.id
        assert result.email == user.email
        assert result.role == user.role
        assert result.profile.first_name == user.profile.first_name
        assert result.profile.last_name == user.profile.last_name

    def test_get_list(self):
        self.service.get_list()

        self.users_repository.get_list.assert_called_once()

    def test_find_own(self):
        user = self.factory.generic('user')
        user.id = ObjectId()

        self.service.find_own(user)

        self.users_repository.find_by_id.assert_called_once_with(user.id)

    def test_search_by_query(self):
        query = 'test@email.com'
        role = 'user'

        items = [self.factory.generic(role)]
        items[0].email = query

        self.page_service.get_page.return_value = Page(items, 1, 1)

        result = self.service.search(1, 10, query, role)

        assert isinstance(result, Page) is True
        assert result.page == 1
        assert result.page_count == 1
        assert len(result.items) == 1
        assert isinstance(result.items[0], User) is True

        self.page_service.get_page.assert_called_once()
