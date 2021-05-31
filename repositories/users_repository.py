from models import User
from .base_repository import BaseRepository
import re


class UsersRepository(BaseRepository):
    def __init__(self, collection, user_translator, indexes) -> None:
        super().__init__(collection, user_translator, [], indexes)

    def get_page(self, skip, limit, role=None) -> list:
        sort = {"$sort": {"_id": -1}}
        match_step = {'$match': {}}
        skip_step = {'$skip': skip}
        limit_step = {'$limit': limit}
        if role:
            match_step['$match'] = {'role': role}

        pipeline = [sort, match_step, skip_step, limit_step]
        return self._find_by_aggregation(self.default_scope + pipeline)

    def count(self, role) -> int:
        find_filter = {}
        if role:
            find_filter['role'] = role
        pipeline = [
            {'$match': find_filter}
        ]
        return self._count_by_aggregation(self.default_scope + pipeline)

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

    def find_password_reset(self, code) -> User or None:
        find_attrs = {
            'password_reset_requests': {
                '$elemMatch': {'code': code}
            }
        }
        pipeline = [
            {'$match': find_attrs}
        ]
        return self._find_one_by_aggregation(self.default_scope + pipeline)

    def search(self, skip: int, limit: int, query: str, role: str) -> list:
        skip_step = {'$skip': skip}
        limit_step = {'$limit': limit}

        search_pipeline = self.__search_pipeline(query, role) + [skip_step, limit_step]
        return self._find_by_aggregation(self.default_scope + search_pipeline)

    def update_last_visit(self, user_id_str, datetime) -> None:
        user_id = self._parse_object_id(user_id_str)
        if not user_id:
            return
        self.collection.update_one({'_id': user_id}, {'$set': {'last_visit_at': datetime}})

    def count_for_search(self, query, role) -> int:
        pipeline = self.__search_pipeline(query, role)
        return self._count_by_aggregation(self.default_scope + pipeline)

    def delete_all(self) -> None:
        super().delete_all()

    def __search_pipeline(self, query, role) -> list:
        return [{
            "$addFields": {
                "name": {
                    "$concat": [
                        {
                            "$ifNull": [
                                "$profile.first_name",
                                ""
                            ]
                        },
                        " ",
                        {
                            "$ifNull": [
                                "$profile.last_name",
                                ""
                            ]
                        }
                    ]
                }
            }}, {
            "$match": {
                "$or": [
                    {
                        "name": {
                            "$regex": query,
                            "$options": "i"
                        }
                    },
                    {
                        "email": {
                            "$regex": re.escape(query),
                            "$options": "i"
                        }
                    }
                ],
                'role': role
            }
        }]
