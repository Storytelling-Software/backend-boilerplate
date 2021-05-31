from validators import PresenceNumericValidator
from validators.base_validator import BaseValidator


class TestPresenceNumericValidator:
    def setup(self):
        self.validator = PresenceNumericValidator(
            'numeric_value'
        )

        assert self.validator.key == 'numeric_value'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_exists_value(self):
        args = {
            'numeric_value': 'value'
        }

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_invalid_missing_value(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is False

    def test_is_valid_invalid_value_zero_length(self):
        args = {
            'numeric_value': ''
        }

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == f'Has to be present'
        assert result['key'] == 'error_presence'
