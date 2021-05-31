from validators import PositiveValidator
from validators.base_validator import BaseValidator


class TestPositiveValidator:
    def setup(self):
        self.validator = PositiveValidator('balance_change')

        assert self.validator.key == 'balance_change'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid(self):
        args = {'balance_change': 5}
        assert self.validator.is_valid(args)

    def test_is_valid_no_value(self):
        args = {}
        assert self.validator.is_valid(args)

    def test_is_valid_negative(self):
        args = {'balance_change': -19}
        assert not self.validator.is_valid(args)

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == f'Number must be positive'
        assert result['key'] == 'error_not_positive_value'
