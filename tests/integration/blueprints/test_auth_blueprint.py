import json
from bson import ObjectId
from structure import structure
from app import app
from tests.factories import UserFactory
from models import TokenPair, PasswordResetRequest
from mock import Mock, patch
from datetime import timedelta


class TestAuthBlueprint:
    def setup(self):
        self.client = app.test_client()
        self.context = app.app_context()
        self.context.push()
        self.factory = UserFactory()
        self.tokens_service = structure.instantiate('tokens_service')
        self.users_repository = structure.instantiate('users_repository')
        self.user_email_service = structure.instantiate('user_email_service')
        self.user_email_service.celery = Mock()
        self.celery_mock = self.user_email_service.celery

    def teardown(self):
        self.context.pop()

    def auth_headers(self):
        auth_service = structure.instantiate('auth_service')
        self.principal.id = self.users_repository.create(self.principal)
        self.principal.token_pairs.append(
            auth_service.login(self.principal.email, 'Qq12345!')
        )
        return {
            'Authorization': 'token ' + self.principal.token_pairs[0].access
        }

    def test_matching_credentials_login(self):
        user = self.factory.generic('student', password='123456')
        user.id = self.users_repository.create(user)

        json_body = {'email': user.email, 'password': '123456'}
        response = self.client.post(
            '/v1/auth/login', json=json_body, content_type='application/json')
        assert response.status_code == 200
        response_body = response.json
        updated_user = self.users_repository.find_by_id(user.id)
        assert len(updated_user.token_pairs) == 1
        assert updated_user.token_pairs[0].access == response_body['access']
        assert updated_user.token_pairs[0].refresh == response_body['refresh']
        for key in ['access', 'refresh']:
            payload = self.tokens_service.decode(response_body[key])
            assert 'id' in payload
            assert 'user_id' in payload
            assert 'role' in payload

    def test_non_matching_credentials_login(self):
        json_body = {'email': 'dunno@whoit.is', 'password': 'butletmein'}
        response = self.client.post(
            '/v1/auth/login', json=json_body, content_type='application/json')
        assert response.status_code == 401

    def test_successful_refresh(self):
        user = self.factory.generic('student', password='123456')
        user.id = self.users_repository.create(user)
        claims = {'id': str(ObjectId()), 'user_id': str(user.id)}
        access = self.tokens_service.encode('access', claims)
        refresh = self.tokens_service.encode('refresh', claims)
        user.token_pairs.append(TokenPair(claims['id'], access, refresh))
        self.users_repository.update(user)
        json_body = {'refresh_token': user.token_pairs[0].refresh}
        response = self.client.post(
            '/v1/auth/refresh', json=json_body, content_type='application/json')
        assert response.status_code == 200
        response_body = response.json
        updated_user = self.users_repository.find_by_id(user.id)
        assert len(updated_user.token_pairs) == 1
        assert updated_user.token_pairs[0].access == response_body['access']
        assert updated_user.token_pairs[0].refresh == response_body['refresh']
        assert updated_user.token_pairs[0].refresh == user.token_pairs[0].refresh
        # returns the same pair if access is valid
        assert access == response_body['access']

    def test_refresh_with_invalid_token(self):
        json_body = {'refresh_token': 'token'}
        response = self.client.post(
            '/v1/auth/refresh', json=json_body, content_type='application/json')
        assert response.status_code == 401

    def test_refresh_with_valid_unknown_token(self):
        user = self.factory.generic('student', password='123456')
        user.id = self.users_repository.create(user)
        claims = {'id': str(ObjectId()), 'user_id': str(user.id)}
        refresh = self.tokens_service.encode('refresh', claims)
        json_body = {'refresh_token': refresh}
        response = self.client.post(
            '/v1/auth/refresh', json=json_body, content_type='application/json')
        assert response.status_code == 401

    def test_successful_logout(self):
        user = self.factory.generic('student', password='123456')
        user.id = self.users_repository.create(user)

        self.generate_token_pairs(user)
        self.generate_token_pairs(user)

        headers = {"authorization": f"Token {user.token_pairs[1].access}"}

        response = self.client.post(
            '/v1/auth/logout', headers=headers, content_type='application/json')
        assert response.status_code == 200

        updated_user = self.users_repository.find_by_id(user.id)
        assert len(updated_user.token_pairs) == 1
        assert updated_user.token_pairs[0].access == user.token_pairs[0].access

    def generate_token_pairs(self, user):
        claims = {'id': str(ObjectId()), 'user_id': str(user.id)}
        access = self.tokens_service.encode('access', claims)
        refresh = self.tokens_service.encode('refresh', claims)
        user.token_pairs.append(TokenPair(claims['id'], access, refresh))
        self.users_repository.update(user)

    def test_request_forgot_password(self):
        user = self.factory.generic('student', password='123456')
        user.id = self.users_repository.create(user)
        
        json_body = {
            'email': user.email
        }

        response = self.client.post('/v1/auth/forgot_password', json=json_body, content_type='application/json')
        assert response.status_code == 200
        assert response.json == {}
        updated_user = self.users_repository.find_by_id(user.id)
        assert len(updated_user.password_reset_requests) > 0
        self.celery_mock.send_task.assert_called_once()

    def test_request_forgot_password_missing_user(self):
        user = self.factory.generic('student', password='123456')
        json_body = {
            'email': user.email
        }

        response = self.client.post('/v1/auth/forgot_password', json=json_body, content_type='application/json')
        assert response.status_code == 200
        assert response.json == {}
        assert not self.celery_mock.send_task.called

    def test_reset_password_valid(self):
        user = self.factory.generic('student', password='123456')
        user.password_reset_requests = [PasswordResetRequest()]
        user.id = self.users_repository.create(user)

        json_body = {
            'new_password': 'qweQWE123',
            'password_confirmation': 'qweQWE123',
            'code': user.password_reset_requests[0].code,
            'email': user.email
        }
        response = self.client.post('/v1/auth/reset_password', json=json_body, content_type='application/json')
        assert response.status_code == 200
        password_service = structure.instantiate('password_service')
        updated_user = self.users_repository.find_by_id(user.id)
        assert password_service.check('qweQWE123', updated_user.password_hash)

    def test_reset_password_wrong_email(self):
        user = self.factory.generic('student', password='123456')
        user.password_reset_requests = [PasswordResetRequest()]
        user.id = self.users_repository.create(user)

        json_body = {
            'new_password': 'qweQWE123',
            'password_confirmation': 'qweQWE123',
            'code': user.password_reset_requests[0].code,
            'email': "email@test.com"
        }
        response = self.client.post('/v1/auth/reset_password', json=json_body, content_type='application/json')
        assert response.status_code == 400
        password_service = structure.instantiate('password_service')
        updated_user = self.users_repository.find_by_id(user.id)
        assert not password_service.check('qweQWE123', updated_user.password_hash)

    def test_reset_password_expired(self):
        user = self.factory.generic('student', password='123456')
        user.password_reset_requests = [PasswordResetRequest()]
        user.password_reset_requests[0].created_at = user.password_reset_requests[0].created_at + timedelta(days=-3)
        user.id = self.users_repository.create(user)

        json_body = {
            'new_password': 'qweQWE123',
            'password_confirmation': 'qweQWE123',
            'code': user.password_reset_requests[0].code,
            'old_password': '123456'
        }
        response = self.client.post('/v1/auth/reset_password', json=json_body, content_type='application/json')
        assert response.status_code == 400
        assert 'message' in response.json['code'][0].keys()
        assert 'key' in response.json['code'][0].keys()
        password_service = structure.instantiate('password_service')
        updated_user = self.users_repository.find_by_id(user.id)
        assert not password_service.check('qweQWE123', updated_user.password_hash)

    def test_reset_password_mismatch(self):
        user = self.factory.generic('student', password='123456')
        user.password_reset_requests = [PasswordResetRequest()]
        user.id = self.users_repository.create(user)

        json_body = {
            'new_password': 'qweQWE123',
            'password_confirmation': 'qweQWE1234',
            'code': user.password_reset_requests[0].code,
            'old_password': '123456'
        }
        response = self.client.post('/v1/auth/reset_password', json=json_body, content_type='application/json')
        assert response.status_code == 400
