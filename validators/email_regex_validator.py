import re

from .base_validator import BaseKeyValidator


class EmailRegexValidator(BaseKeyValidator):
    def is_valid(self, args: dict) -> bool:
        if self.key not in args or not args[self.key]:
            return True
        value = args[self.key]
        # Match: @ sign, and at least one . in the part after the @ w/o white spaces
        if re.match(r'^[^\s]+@[^\s]+\.[^\s]+$', value):
            return True
        return False

    def error(self) -> dict:
        return {
            'message': 'Invalid format',
            'key': 'error_email_invalid_format'
        }
