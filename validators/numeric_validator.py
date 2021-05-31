from .base_validator import BaseKeyValidator


class NumericValidator(BaseKeyValidator):
    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key)
        if not value:
            return True
        return type(value) in [int, float]

    def error(self) -> dict:
        return {
            'message': f'Must be a number',
            'key': 'error_invalid_format'
        }
