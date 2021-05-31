from .base_validator import BaseKeyValidator
from datetime import datetime


class StringDateValidator(BaseKeyValidator):
    def __init__(self, key) -> None:
        super().__init__(key)

    def is_valid(self, args) -> bool:
        value = args.get(self.key)
        if not value:
            return True
        try:
            correct_date = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return False
        return correct_date is not None

    def error(self) -> dict:
        return {
            'message': 'Should be YYYY-MM-DD',
            'key': 'error_invalid_format'
        }
