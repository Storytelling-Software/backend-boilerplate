from .base_validator import BaseKeyValidator


class PasswordsMatchValidator(BaseKeyValidator):
    def __init__(self, key, matching_key) -> None:
        super().__init__(key)
        self.matching_key = matching_key

    def is_valid(self, args: dict) -> bool:
        return args[self.key] == args[self.matching_key]

    def error(self) -> dict:
        return {
            'message': 'Passwords should match',
            'key': 'error_password_mismatch'
        }
