from validators import PasswordsMatchValidator
from validators.base_validator import BaseValidator


class TestPasswordMatchValidator:
    def setup(self):
        self.validator = PasswordsMatchValidator('new_password', 'password_confirmation')
        assert self.validator.key == 'new_password'
        assert self.validator.matching_key == 'password_confirmation'
        assert isinstance(self.validator, BaseValidator) is True

    def test_is_valid_invalid_mismatched_password(self):
        args = {
            'new_password': 'Qq12345!',
            'password_confirmation': 'Qq1234!'
        }
        result = self.validator.is_valid(args)
        assert result is False

    def test_is_valid_matched_password(self):
        args = {
            'new_password': 'Qq12345!',
            'password_confirmation': 'Qq12345!'
        }
        result = self.validator.is_valid(args)
        assert result is True

    def test_error_message(self):
        result = self.validator.error()
        assert result['message'] == 'Passwords should match'
        assert result['key'] == 'error_password_mismatch'
