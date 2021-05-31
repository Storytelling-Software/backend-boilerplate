from .base_validator import BaseKeyValidator


class PresenceValidator(BaseKeyValidator):
    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key)
        return value is not None and len(value) > 0

    def error(self) -> dict:
        return {
            'message': 'Has to be present',
            'key': 'error_presence'
        }
