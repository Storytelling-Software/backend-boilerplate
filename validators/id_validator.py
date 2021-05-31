from .base_validator import BaseKeyValidator
from bson import ObjectId


class IdValidator(BaseKeyValidator):
    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key)
        if not value:
            return True
        return ObjectId.is_valid(value)

    def error(self) -> dict:
        return {
            'message': 'Has to be a valid ID',
            'key': 'error_invalid_id'
        }
