from mock import Mock

from validators import NameUniqueValidator
from validators.base_validator import BaseValidator


class TestNameUniqueValidator:
    def setup(self):
        self.users_repository_mock = Mock()

        self.validator = NameUniqueValidator(
            'name',
            self.users_repository_mock
        )

        assert self.validator.key == 'name'
        assert self.validator.repository == self.users_repository_mock
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_already_exists(self):
        user_mock = Mock()
        self.users_repository_mock.find_by_name.return_value = user_mock

        args = {'name': 'John'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_is_valid_unique(self):
        self.users_repository_mock.find_by_name.return_value = None
        args = {'name': 'Jane'}

        result = self.validator.is_valid(args)

        assert result is True

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == 'Already exists'
        assert result['key'] == 'error_already_exists'
