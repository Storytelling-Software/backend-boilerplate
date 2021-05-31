from .base_validator import BaseKeyValidator


class NegativeValidator(BaseKeyValidator):
    def __init__(self, key: str) -> None:
        super().__init__(key)

    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key)
        if type(value) != int:
            return True
        return value < 0

    def error(self) -> dict:
        return {
            'message': 'Number must be negative',
            'key': 'error_not_negative_value'
        }
