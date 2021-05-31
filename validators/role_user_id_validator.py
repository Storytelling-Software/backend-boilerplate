from .base_validator import BaseKeyValidator


class RoleUserIdValidator(BaseKeyValidator):
    def __init__(self, key, users_repository, role) -> None:
        super().__init__(key)
        self.users_repository = users_repository
        self.role = role

    def is_valid(self, args: dict) -> bool:
        value = args.get(self.key, '')
        user = self.users_repository.find_by_id(value)
        if not user:
            return False
        return user.role == self.role

    def error(self) -> dict:
        return {
            'message': f'Invalid {self.role} id',
            'key': 'error_invalid_role'
        }
