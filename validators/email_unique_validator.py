from .base_validator import BaseKeyValidator


class EmailUniqueValidator(BaseKeyValidator):
    def __init__(self, key: str, users_repository) -> None:
        super().__init__(key)
        self.users_repository = users_repository

    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key, '')
        return self.users_repository.find_by_email(value) is None

    def error(self) -> dict:
        return {
            'message': 'Already taken',
            'key': 'error_email_already_taken'
        }
