from validators import LengthValidator
from validators.base_validator import BaseValidator


class TestLengthValidator:
    def setup(self):
        self.validator = LengthValidator('password', 8, 32)

        assert self.validator.key == 'password'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_invalid_len_0(self):
        args = {'password': ''}
        assert not self.validator.is_valid(args)

    def test_is_valid_invalid_len_7(self):
        args = {'password': '1234567'}
        assert not self.validator.is_valid(args)

    def test_is_valid_valid_len_8(self):
        args = {'password': '12345678'}
        assert self.validator.is_valid(args)

    def test_is_valid_valid_len_32(self):
        args = {'password': '12345678901234567890123456789012'}
        assert self.validator.is_valid(args)

    def test_is_valid_invalid_len_33(self):
        args = {'password': '123456789012345678901234567890123'}
        assert not self.validator.is_valid(args)

    def test_error(self):
        result = self.validator.error()
        assert result['message'] == 'Length must be between 8 and 32'
        assert result['key'] == 'error_invalid_length'
