from validators import IdListValidator
from validators.base_validator import BaseValidator

from bson import ObjectId


class TestIdListValidator:
    def setup(self):
        self.validator = IdListValidator(
            'categories'
        )

        assert self.validator.key == 'categories'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_id_list(self):
        args = {'categories': [str(ObjectId())]}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_no_value(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_invalid_id_list(self):
        args = {'categories': ['1234']}

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        self.validator.errors = ['Some invalid ID']
        result = self.validator.error()

        assert result['message'] == f'Must be valid IDs: {self.validator.errors}'
        assert result['key'] == 'error_invalid_id'
