from validators import PresenceValidator
from validators.base_validator import BaseValidator


class TestPresenceValidator:
    def setup(self):
        self.validator = PresenceValidator(
            'user_id'
        )

        assert self.validator.key == 'user_id'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_value_exists(self):
        args = {
            'user_id': 'some_value'
        }

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_invalid_missing_value(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is False

    def test_is_valid_invalid_value_zero_length(self):
        args = {
            'user_id': ''
        }

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == f'Has to be present'
        assert result['key'] == 'error_presence'
