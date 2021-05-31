from .base_validator import BaseKeyValidator


class UserIdValidator(BaseKeyValidator):
    def __init__(self, key, users_repository) -> None:
        super().__init__(key)
        self.users_repository = users_repository

    def is_valid(self, args) -> bool:
        value = args.get(self.key)
        if not value:
            return True
        user = self.users_repository.find_by_id(value)
        return user is not None

    def error(self) -> dict:
        return {
            'message': 'Should be a valid user id',
            'key': 'error_invalid_user_id'
        }
