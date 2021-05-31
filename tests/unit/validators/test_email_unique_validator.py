from mock import Mock

from validators import EmailUniqueValidator
from validators.base_validator import BaseValidator


class TestEmailUniqueValidator:
    def setup(self):
        self.users_repository_mock = Mock()

        self.validator = EmailUniqueValidator(
            'email',
            self.users_repository_mock
        )

        assert self.validator.key == 'email'
        assert self.validator.users_repository == self.users_repository_mock
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_already_exists(self):
        user_mock = Mock()
        self.users_repository_mock.find_by_email.return_value = user_mock

        args = {'email': 'asd123.321@example3.co'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_is_valid_unique(self):
        self.users_repository_mock.find_by_email.return_value = None
        args = {'email': 'asd123.321@example3.co'}

        result = self.validator.is_valid(args)

        assert result is True

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == 'Already taken'
        assert result['key'] == 'error_email_already_taken'
