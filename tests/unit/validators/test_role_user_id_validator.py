from mock import Mock

from validators.role_user_id_validator import RoleUserIdValidator
from validators.base_validator import BaseValidator
from ...factories.user import UserFactory


class TestRoleUserIdValidator:
    def setup(self):
        self.users_repository_mock = Mock()
        self.role = 'user'
        self.factory = UserFactory()

        self.validator = RoleUserIdValidator(
            'role',
            self.users_repository_mock,
            self.role
        )

        assert self.validator.key == 'role'
        assert self.validator.users_repository == self.users_repository_mock
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_valid(self):
        user = self.factory.generic('user')
        args = {
            'role': 'user'
        }
        self.users_repository_mock.find_by_id.return_value = user

        result = self.validator.is_valid(args)

        self.users_repository_mock.find_by_id.assert_called_once_with('user')
        assert result is True

    def test_is_valid_wrong_role(self):
        admin = self.factory.generic('admin')
        args = {
            'role': 'admin'
        }
        self.users_repository_mock.find_by_id.return_value = admin

        result = self.validator.is_valid(args)

        self.users_repository_mock.find_by_id.assert_called_once_with('admin')
        assert result is False

    def test_is_valid_missing_user(self):
        args = {
            'role': 'user'
        }
        self.users_repository_mock.find_by_id.return_value = None

        result = self.validator.is_valid(args)

        self.users_repository_mock.find_by_id.assert_called_once_with('user')
        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == 'Invalid user id'
        assert result['key'] == 'error_invalid_role'
