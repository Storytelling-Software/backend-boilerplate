from validators import EmailRegexValidator
from validators.base_validator import BaseValidator


class TestEmailRegexValidator:
    def setup(self):
        self.validator = EmailRegexValidator('email')

        assert self.validator.key == 'email'
        assert isinstance(self.validator, BaseValidator) is True

    def test_no_value_is_valid(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_invalid(self):
        args = {'email': '!^&bh1asd12312.c'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_is_valid_invalid_white_spaces(self):
        args = {'email': 'aaa @a sd12312.com'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_is_valid_valid(self):
        args = {'email': 'asd123.321@example3.co'}

        result = self.validator.is_valid(args)

        assert result is True

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == 'Invalid format'
        assert result['key'] == 'error_email_invalid_format'
