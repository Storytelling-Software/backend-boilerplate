from mock import Mock

from validators import UserIdValidator
from validators.base_validator import BaseValidator


class TestUserIdValidator:
    def setup(self):
        self.users_repository_mock = Mock()

        self.validator = UserIdValidator(
            'user_id',
            self.users_repository_mock
        )

        assert self.validator.key == 'user_id'
        assert self.validator.users_repository == self.users_repository_mock
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_user_exists(self):
        user_mock = Mock()
        self.users_repository_mock.find_by_id.return_value = user_mock

        args = {'user_id': 'User ID'}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_no_value(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_user_missing(self):
        self.users_repository_mock.find_by_id.return_value = None

        args = {'user_id': 'some id'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == 'Should be a valid user id'
        assert result['key'] == 'error_invalid_user_id'
