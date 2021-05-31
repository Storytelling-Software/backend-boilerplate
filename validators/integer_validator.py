from .base_validator import BaseKeyValidator


class IntegerValidator(BaseKeyValidator):
    def __init__(self, key: str) -> None:
        super().__init__(key)

    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key, '')
        if not value:
            return True
        return isinstance(value, int)

    def error(self) -> dict:
        return {
            'message': 'Must be an integer',
            'key': 'error_type_integer'
        }
