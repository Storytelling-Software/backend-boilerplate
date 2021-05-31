from validators import IdValidator
from validators.base_validator import BaseValidator

from bson import ObjectId


class TestIdValidator:
    def setup(self):
        self.validator = IdValidator(
            'retailer_id'
        )

        assert self.validator.key == 'retailer_id'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_id_list(self):
        args = {'retailer_id': str(ObjectId())}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_no_value(self):
        args = {}

        result = self.validator.is_valid(args)

        assert result is True

    def test_is_valid_invalid_id(self):
        args = {'retailer_id': '1234'}

        result = self.validator.is_valid(args)

        assert result is False

    def test_error(self):
        result = self.validator.error()

        assert result['message'] == f'Has to be a valid ID'
        assert result['key'] == 'error_invalid_id'
