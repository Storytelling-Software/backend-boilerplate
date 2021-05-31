from .base_validator import BaseKeyValidator


class LengthValidator(BaseKeyValidator):
    def __init__(self, key, min_value, max_value) -> None:
        super().__init__(key)
        self.min_value = min_value
        self.max_value = max_value

    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key, '')
        return self.min_value <= len(value) <= self.max_value

    def error(self) -> dict:
        return {
            'message': f'Length must be between {self.min_value} and {self.max_value}',
            'key': 'error_invalid_length'
        }
