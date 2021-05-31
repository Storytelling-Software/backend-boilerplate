from .base_repository import BaseRepository
import re


class UserApplicationsRepository(BaseRepository):
    def __init__(self, collection, user_translator, indexes) -> None:
        super().__init__(collection, user_translator, [], indexes)

    def find_by_email(self, email: str) -> list or None:
        escaped_email = re.escape(email)
        find_attrs = {
            'email': {
                '$regex': f'^{escaped_email}$',
                '$options': 'i'
            }
        }
        pipeline = [
            {'$match': find_attrs}
        ]
        return self._find_one_by_aggregation(self.default_scope + pipeline)
