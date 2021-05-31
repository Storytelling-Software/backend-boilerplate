from validators import NumericValidator
from validators.base_validator import BaseValidator


class TestNumericValidator:
    def setup(self):
        self.validator = NumericValidator('value')

        assert self.validator.key == 'value'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_int(self):
        args = {'value': 5}
        assert self.validator.is_valid(args)

    def test_is_valid_no_value(self):
        args = {}
        assert self.validator.is_valid(args)

    def test_is_valid_float(self):
        args = {'value': 5.6}
        assert self.validator.is_valid(args)

    def test_is_valid_string(self):
        args = {'value': '12345678'}
        assert not self.validator.is_valid(args)

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == f'Must be a number'
        assert result['key'] == 'error_invalid_format'
