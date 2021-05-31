from .base_validator import BaseKeyValidator
from bson import ObjectId


class IdListValidator(BaseKeyValidator):
    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.errors = None

    def is_valid(self, args: dict) -> bool:
        self.errors = []
        values = args.get(self.key)
        if not values:
            return True
        for value in values:
            if ObjectId.is_valid(value):
                continue
            self.errors.append(value)
        return len(self.errors) == 0

    def error(self) -> dict:
        return {
            'message': f'Must be valid IDs: {self.errors}',
            'key': 'error_invalid_id'
        }
