from .base_validator import BaseKeyValidator


class ListTypeValidator(BaseKeyValidator):
    def is_valid(self, args) -> bool:
        return type(args) == list

    def error(self) -> dict:
        return {
            'message': 'Has to be a list',
            'key': 'error_invalid_type'
        }
