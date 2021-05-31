from validators import ListTypeValidator
from validators.base_validator import BaseValidator


class TestListTypeValidator:
    def setup(self):
        self.validator = ListTypeValidator(
            'cashout_attr'
        )

        assert self.validator.key == 'cashout_attr'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_list(self):
        args = [
            'some_attr'
        ]

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_invalid_not_list(self):
        args = {'cashout_dict': 'some_value'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == f'Has to be a list'
        assert result['key'] == 'error_invalid_type'
