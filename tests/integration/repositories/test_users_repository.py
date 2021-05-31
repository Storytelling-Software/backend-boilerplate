import os

import pymongo
from bson import ObjectId

from models import User, Profile
from tests.factories import UserFactory
from structure import structure
users_repository = structure.instantiate('users_repository')


class TestUsersRepository:
    def setup(self):
        scheme = os.environ['MONGO_SCHEME']
        username = os.environ['MONGO_USERNAME']
        password = os.environ['MONGO_PASSWORD']
        host = os.environ['MONGO_HOST']
        port = os.environ['MONGO_PORT']
        name = os.environ['MONGO_NAME']
        url = f'{scheme}://{username}:{password}@{host}:{port}'
        self.client = pymongo.MongoClient(url)
        self.collection = self.client[name]['users']

        self.factory = UserFactory()
        self.repository = users_repository

    def teardown(self):
        self.collection.delete_many({})
        self.client.close()

    def test_create(self):
        user = User()
        user.id = None
        user.email = 'my@example.com'
        user.phone_number = '+1234567890'
        user.role = 'user'
        user.password_hash = b'my top secret'
        user.token_pairs = []
        user.password_reset_requests = []
        user_profile = Profile()
        user_profile.first_name = 'John'
        user_profile.last_name = 'Doe'
        user.profile = user_profile

        result = self.repository.create(user)

        assert isinstance(result, ObjectId) is True

        user_from_db = self.collection.find_one({'_id': result})
        assert user_from_db['_id'] == result
        assert user_from_db['email'] == user.email
        assert user_from_db['role'] == user.role
        assert user_from_db['password_hash'] == user.password_hash
        assert user_from_db['token_pairs'] == user.token_pairs
        assert user_from_db['profile']['first_name'] == user.profile.first_name
        assert user_from_db['profile']['last_name'] == user.profile.last_name

    def test_find_by_email_none(self):
        email = 'user@example.com'

        result = self.repository.find_by_email(email)

        assert result is None

    def test_find_password_reset(self):
        code = 'test_code'
        result = self.repository.find_password_reset(code)

        assert result is None

    def test_find_by_email(self):
        user = User()
        user.id = None
        user.email = 'my@example.com'
        user.phone_number = '+1234567890'
        user.role = 'user'
        user.password_hash = b'my top secret'
        user.token_pairs = []
        user.password_reset_requests = []
        user_profile = Profile()
        user_profile.first_name = 'John'
        user_profile.last_name = 'Doe'
        user.profile = user_profile

        user_id = self.collection.insert_one(
            self.repository.model_translator.to_document(user)
        ).inserted_id

        result = self.repository.find_by_email(user.email)

        assert isinstance(result, User) is True
        assert result.id == user_id
        assert result.email == user.email
        assert result.role == user.role
        assert result.password_hash == user.password_hash
        assert result.token_pairs == user.token_pairs
        assert result.profile.first_name == user.profile.first_name
        assert result.profile.last_name == user.profile.last_name

    def test_get_page(self):
        for _ in range(12):
            self.repository.create(self.factory.generic('user'))

        skip = 5
        limit = 10
        role = 'user'

        result = self.repository.get_page(skip, limit, role)

        assert isinstance(result, list) is True
        assert len(result) == 7

    def test_get_page_empty(self):
        skip = 10
        limit = 10
        role = 'user'

        result = self.repository.get_page(skip, limit, role)

        assert isinstance(result, list) is True
        assert len(result) == 0

    def test_get_page_empty_out_of_range(self):
        for _ in range(12):
            self.repository.create(self.factory.generic('user'))

        skip = 12
        limit = 50
        role = 'user'

        result = self.repository.get_page(skip, limit, role)

        assert isinstance(result, list) is True
        assert len(result) == 0

    def test_search_by_query_by_email(self):
        user1 = User()
        user1.id = ObjectId()
        user1.email = 'my1@example.com'
        user1.role = 'user'
        user1.password_hash = b'my top secret'
        user1.token_pairs = []
        user1.password_reset_requests = []
        user_profile = Profile()
        user_profile.first_name = 'John'
        user_profile.last_name = 'Doe'
        user1.profile = user_profile
        user_id1 = self.collection.insert_one(
            self.repository.model_translator.to_document(user1)
        ).inserted_id

        user2 = User()
        user2.id = ObjectId()
        user2.email = 'my1@example.com'
        user2.role = 'user'
        user2.password_hash = b'my top secret'
        user2.token_pairs = []
        user2.password_reset_requests = []
        user_profile = Profile()
        user_profile.first_name = 'Jane'
        user_profile.last_name = 'Miller'
        user2.profile = user_profile
        user_id2 = self.collection.insert_one(
            self.repository.model_translator.to_document(user2)
        ).inserted_id

        skip = 0
        limit = 10
        query = user1.profile.first_name
        role = user1.role

        result = self.repository.search(skip, limit, query, role)

        assert isinstance(result, list) is True
        assert len(result) == 1
        assert isinstance(result[0], User) is True
        assert result[0].id == user_id1

    def test_search_by_query_by_part_of_full_name(self):
        user1 = User()
        user1.id = ObjectId()
        user1.email = 'my1@example.com'
        user1.role = 'user'
        user1.password_hash = b'my top secret'
        user1.token_pairs = []
        user1.password_reset_requests = []
        user_profile = Profile()
        user_profile.first_name = 'John'
        user_profile.last_name = 'Doe'
        user1.profile = user_profile
        user_id1 = self.collection.insert_one(
            self.repository.model_translator.to_document(user1)
        ).inserted_id

        user2 = User()
        user2.id = ObjectId()
        user2.email = 'my1@example.com'
        user2.role = 'user'
        user2.password_hash = b'my top secret'
        user2.token_pairs = []
        user2.password_reset_requests = []
        user_profile = Profile()
        user_profile.first_name = 'Jane'
        user_profile.last_name = 'Miller'
        user2.profile = user_profile
        user_id2 = self.collection.insert_one(
            self.repository.model_translator.to_document(user2)
        ).inserted_id

        skip = 0
        limit = 10
        query = 'ane mil'
        role = user1.role

        result = self.repository.search(skip, limit, query, role)

        assert isinstance(result, list) is True
        assert len(result) == 1
        assert isinstance(result[0], User) is True
        assert result[0].id == user_id2

    def test_search_by_query_no_users(self):
        skip = 0
        limit = 10
        query = 'ane mil'
        role = 'user'

        result = self.repository.search(skip, limit, query, role)

        assert isinstance(result, list) is True
        assert len(result) == 0
