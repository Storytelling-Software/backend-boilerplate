from validators import StringDateValidator
from validators.base_validator import BaseValidator


class TestStringDateValidator:
    def setup(self):

        self.validator = StringDateValidator(
            'purchase_date'
        )

        assert self.validator.key == 'purchase_date'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_correct_date(self):
        args = {'purchase_date': '2020-01-01'}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_no_date(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_incorrect_date(self):
        args = {'purchase_date': '2020-02-31'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == 'Should be YYYY-MM-DD'
        assert result['key'] == 'error_invalid_format'
