from .base_validator import BaseKeyValidator


class NameUniqueValidator(BaseKeyValidator):
    def __init__(self, key: str, repository) -> None:
        super().__init__(key)
        self.repository = repository

    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key, '')
        return self.repository.find_by_name(value) is None

    def error(self) -> dict:
        return {
            'message': 'Already exists',
            'key': 'error_already_exists'
        }
