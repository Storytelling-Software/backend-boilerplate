from app import app
from structure import structure
from tests.factories import UserFactory
from models import User, UserApplication

from io import BytesIO
from bson import ObjectId
from mock import Mock
from faker import Faker
from datetime import datetime


class TestUsersBlueprint:
    def setup(self):
        self.client = app.test_client()
        self.context = app.app_context()
        self.context.push()
        self.faker = Faker()
        self.user_factory = UserFactory()
        self.users_repository = structure.instantiate('users_repository')
        self.user_applications_repository = structure.instantiate('user_applications_repository')
        self.principal = self.user_factory.generic('admin')
        # self.email_list_service = structure.instantiate('email_list_service')
        self.email_list_service = structure.instantiate('email_list_service_mocking')
        self.email_list_service.mailchimp_client = Mock()
        self.user_files_s3_wrapper = structure.instantiate('user_file_s3_wrapper')
        self.user_temp_files_s3_wrapper = structure.instantiate('user_temp_file_s3_wrapper')
        self.user_email_service = structure.instantiate('user_email_service')
        self.user_email_service.celery = Mock()
        self.files = []

    def teardown(self):
        for file in self.files: # change after s3 setups
            pass
            # self.user_files_s3_wrapper.delete(file['key'])
            # self.user_temp_files_s3_wrapper.delete(file['key'])

        self.files = []

        self.context.pop()
        self.users_repository.delete_all()
        self.user_applications_repository.delete_all()

    def auth_headers(self):
        auth_service = structure.instantiate('auth_service')
        self.principal.id = self.users_repository.create(self.principal)
        self.principal.token_pairs.append(
            auth_service.login(self.principal.email, 'Qq12345!')
        )
        self.users_repository.update(self.principal)
        return {
            'Authorization': 'token ' + self.principal.token_pairs[0].access
        }

    def auth_headers_user(self, user):
        auth_service = structure.instantiate('auth_service')
        user.token_pairs.append(
            auth_service.login(user.email, 'Qq12345!')
        )
        self.users_repository.update(user)
        return {
            'Authorization': 'token ' + user.token_pairs[0].access
        }

    def test_create_user_valid(self):
        json_body = {
            'email': self.faker.email(),
            'password': 'qweQWE123',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        }
        response = self.client.post('/v1/users/signup', json=json_body)
        assert response.status_code == 200
        application = self.user_applications_repository.find_by_email(json_body['email'])
        assert application is not None
        assert application.role == 'user'
        user = self.users_repository.find_by_email(json_body['email'])
        assert user is None

    def test_create_user_valid_missing_profile(self):
        json_body = {
            'email': self.faker.email(),
            'password': 'qweQWE123'
        }
        response = self.client.post('/v1/users/signup', json=json_body)
        assert response.status_code == 200
        application = self.user_applications_repository.find_by_email(json_body['email'])
        assert application is not None
        assert application.role == 'user'
        user = self.users_repository.find_by_email(json_body['email'])
        assert user is None

    def test_create_user_invalid(self):
        json_body = {
            'email': self.faker.email(),
            'password': 'qwe',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        }
        response = self.client.post('/v1/users/signup', json=json_body)
        assert response.status_code == 400

    def test_create_user_existing_application(self):
        user_application = UserApplication.from_request({
            'email': self.faker.email(),
            'password_hash': '',
            'role': 'user',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        })
        user_application.id = self.user_applications_repository.create(user_application)
        existing_user_application = self.user_applications_repository.find_by_email(user_application.email)

        json_body = {
            'email': user_application.email,
            'password': 'qweQWE123',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        }
        response = self.client.post('/v1/users/signup', json=json_body)
        assert response.status_code == 200
        found_user_application = self.user_applications_repository.find_by_email(json_body['email'])

        assert found_user_application.id == existing_user_application.id
        assert found_user_application.email == existing_user_application.email
        assert found_user_application.code == existing_user_application.code
        assert found_user_application.profile.first_name == json_body['profile']['first_name']
        assert found_user_application.profile.last_name == json_body['profile']['last_name']

    def test_create_user_existing_email(self):
        existing = self.user_factory.generic('user')
        existing.id = self.users_repository.create(existing)
        json_body = {
            'email': existing.email,
            'password': 'qweQWE123',
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name()
        }
        response = self.client.post('/v1/users/signup', json=json_body)
        assert response.status_code == 400
        assert response.json['email'][0]['message'] == 'Already taken'

    def test_get_page(self):
        first_user = self.user_factory.generic('user')
        self.users_repository.create(first_user)

        second_user = self.user_factory.generic('user')
        self.users_repository.create(second_user)

        third_user = self.user_factory.generic('user')
        self.users_repository.create(third_user)

        response = self.client.get(
            '/v1/users?role=user',
            headers=self.auth_headers()
        )

        assert response.status_code == 200
        assert isinstance(response.json, dict) is True
        assert isinstance(response.json.get('items'), list) is True
        assert len(response.json.get('items')) == 3

    def test_get_page_anonymous(self):
        response = self.client.get(
            '/v1/users?role=user'
        )
        assert response.status_code == 401

    def test_get_page_by_user(self):
        self.principal = self.user_factory.generic('user')
        response = self.client.get(
            '/v1/users?role=user',
            headers=self.auth_headers()
        )

        assert response.status_code == 403

    def test_search_by_query(self):
        first_user = self.user_factory.generic('user')
        first_user.profile.first_name = 'John'
        first_user.profile.last_name = 'Doe'
        self.users_repository.create(first_user)

        second_user = self.user_factory.generic('user')
        second_user.profile.first_name = 'John'
        second_user.profile.last_name = 'Doehn'
        self.users_repository.create(second_user)

        third_user = self.user_factory.generic('user')
        third_user.profile.first_name = 'Jane'
        third_user.profile.last_name = 'Doe'
        self.users_repository.create(third_user)

        response = self.client.get(
            '/v1/users/search?query=john do&role=user',
            headers=self.auth_headers()
        )

        assert response.status_code == 200
        assert isinstance(response.json, dict) is True
        assert isinstance(response.json.get('items'), list) is True
        assert len(response.json.get('items')) == 2

    def test_search_by_query_no_role(self):
        first_user = self.user_factory.generic('admin')
        first_user.profile.first_name = 'John'
        first_user.profile.last_name = 'Doe'
        self.users_repository.create(first_user)

        second_user = self.user_factory.generic('user')
        second_user.profile.first_name = 'John'
        second_user.profile.last_name = 'Doe'
        self.users_repository.create(second_user)

        response = self.client.get(
            '/v1/users/search?query=john doe',
            headers=self.auth_headers()
        )

        assert response.status_code == 200
        assert isinstance(response.json, dict) is True
        assert isinstance(response.json.get('items'), list) is True
        assert len(response.json.get('items')) == 1

    def test_search_by_query_by_user(self):
        first_user = self.user_factory.generic('user')
        first_user.profile.first_name = 'John'
        first_user.profile.last_name = 'Doe'
        self.users_repository.create(first_user)

        self.principal = self.user_factory.generic('user')

        response = self.client.get(
            '/v1/users/search?query=john do&role=user',
            headers=self.auth_headers()
        )

        assert response.status_code == 403

    def test_search_by_query_anonymous(self):
        response = self.client.get(
            '/v1/users/search?query=john do&role=user'
        )
        assert response.status_code == 401

    def test_get_me_anonymous(self):
        response = self.client.get('/v1/users/me')
        assert response.status_code == 401

    def test_get_users_me_auth(self):
        response = self.client.get('/v1/users/me', headers=self.auth_headers())
        assert response.status_code == 200
        assert response.json.get('profile', {}).get('first_name') == self.principal.profile.first_name

    def test_get_user_by_admin(self):
        existing_user = self.user_factory.generic('user')
        existing_user.last_visit_at = datetime.utcnow()
        existing_user.id = self.users_repository.create(existing_user)

        response = self.client.get(f'/v1/users/{existing_user.id}', headers=self.auth_headers())
        assert response.status_code == 200

    def test_get_user_by_user(self):
        self.principal = self.user_factory.generic('user')
        existing_user = self.user_factory.generic('user')
        existing_user.id = self.users_repository.create(existing_user)

        response = self.client.get(f'/v1/users/{existing_user.id}', headers=self.auth_headers())
        assert response.status_code == 403

    def test_create_admin_valid(self):
        json_body = {
            'email': self.faker.email(),
            'profile': {
                'fist_name': 'John',
                'lst_name': 'Doe'
            }
        }
        response = self.client.post('/v1/admins', json=json_body, headers=self.auth_headers())

        assert response.status_code == 200
        admin = self.users_repository.find_by_email(json_body['email'])
        assert admin is not None
        assert admin.role == 'admin'

    def test_create_admin_anonymous(self):
        json_body = {
            'email': self.faker.email(),
            'profile': {
                'fist_name': 'John',
                'lst_name': 'Doe'
            }
        }
        response = self.client.post('/v1/admins', json=json_body)

        assert response.status_code == 401

    def test_create_admin_invalid(self):
        json_body = {
            'email': '',
            'profile': {
                'fist_name': 'UPD John',
                'lst_name': 'Doe'
            }
        }
        response = self.client.post('/v1/admins', json=json_body, headers=self.auth_headers())

        assert response.status_code == 400

    def test_missing_admin_update(self):
        admin_id = str(ObjectId())
        json_body = {
            'email': 'updated@email.com',
            'profile': {
                'fist_name': 'UPD John',
                'lst_name': 'UPD Doe'
            }
        }
        response = self.client.put(
            f'/v1/users/{admin_id}', json=json_body, headers=self.auth_headers())
        assert response.status_code == 404

    def test_update_admin_with_other_admin_email(self):
        existing_admin = self.user_factory.generic('admin')
        existing_admin.id = self.users_repository.create(existing_admin)

        admin = self.user_factory.generic('admin')
        admin.id = self.users_repository.create(admin)

        json_body = {
            'email': existing_admin.email,
            'profile': {
                'fist_name': 'UPD John',
                'lst_name': 'UPD Doe'
            }
        }

        response = self.client.put(
            f'/v1/users/{str(admin.id)}', json=json_body, headers=self.auth_headers())
        assert response.status_code == 400

    def test_update_admin(self):
        existing_admin = self.user_factory.generic('admin')
        existing_admin.id = self.users_repository.create(existing_admin)

        json_body = {
            'email': 'paul009@yandex.ru',
            'profile': {
                'fist_name': 'UPD John',
                'lst_name': 'UPD Doe'
            }
        }

        response = self.client.put(
            f'/v1/users/{str(existing_admin.id)}', json=json_body, headers=self.auth_headers())
        assert response.status_code == 200

    def test_missing_admin_delete(self):
        user_id = str(ObjectId())
        response = self.client.delete(
            f'/v1/users/{user_id}', headers=self.auth_headers())
        assert response.status_code == 404

    def test_delete_admin(self):
        existing_admin = self.user_factory.generic('admin')
        existing_admin.id = self.users_repository.create(existing_admin)

        response = self.client.delete(
            f'/v1/users/{str(existing_admin.id)}', headers=self.auth_headers())
        assert response.status_code == 200

        deleted_admin = self.users_repository.find_by_id(existing_admin.id)
        assert not deleted_admin

    def test_confirm_registration_valid(self):
        user_application = UserApplication.from_request({
            'email': self.faker.email(),
            'password_hash': '',
            'role': 'user',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        })
        user_application.id = self.user_applications_repository.create(user_application)

        json_body = {
            'email': user_application.email,
            'code': user_application.code
        }
        response = self.client.post('/v1/users/confirmation', json=json_body)
        assert response.status_code == 200
        application = self.user_applications_repository.find_by_email(user_application.email)
        assert application is None
        user = self.users_repository.find_by_email(user_application.email)
        assert user is not None

    def test_confirm_registration_missing(self):
        json_body = {
            'email': self.faker.email(),
            'code': 'ABCDEF'
        }
        response = self.client.post('/v1/users/confirmation', json=json_body)
        assert response.status_code == 400
        assert 'message' in response.json['code'][0].keys()
        assert 'key' in response.json['code'][0].keys()

    def test_confirm_registration_invalid_code(self):
        user_application = UserApplication.from_request({
            'email': self.faker.email(),
            'password_hash': '',
            'role': 'user',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        })
        user_application.id = self.user_applications_repository.create(user_application)

        json_body = {
            'email': user_application.email,
            'code': 'user_application.code'
        }
        response = self.client.post('/v1/users/confirmation', json=json_body)
        assert response.status_code == 400
        user = self.users_repository.find_by_email(user_application.email)
        assert user is None

    def test_confirm_registration_resend_code(self):
        user_application = UserApplication.from_request({
            'email': self.faker.email(),
            'password_hash': '',
            'role': 'user',
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name()
            }
        })
        user_application.id = self.user_applications_repository.create(user_application)

        json_body = {
            'email': user_application.email
        }
        old_code = user_application.code
        response = self.client.post('/v1/users/confirmation/resend', json=json_body)
        assert response.status_code == 200
        user_application = self.user_applications_repository.find_by_email(user_application.email)
        assert user_application.code != old_code

    def test_change_password_valid(self):
        self.principal = self.user_factory.generic('student')
        self.principal.id = self.users_repository.create(self.principal)
        json_body = {
            'old_password': 'Qq12345!',
            'new_password': 'fghFGH1!',
        }

        response = self.client.post(
            f'/v1/users/{self.principal.id}/change_password',
            json=json_body,
            headers=self.auth_headers(),
            content_type='application/json'
        )
        assert response.status_code == 200

    def user_avatar_upload_and_update(self): # add test_ prefix only after s3 setups
        user = self.user_factory.generic('user')
        user.id = self.users_repository.create(user)

        avatar = "fake-avatar-stream.jpg"
        data = {
            'file': (BytesIO(b"some initial avatar data"), avatar)
        }
        file_upload_response = self.client.post(
            '/v1/users/files',
            headers=self.auth_headers(),
            data=data)
        file_json_response = file_upload_response.json
        self.files.append(file_json_response)

        json_body = {
            'email': self.faker.email(),
            'profile': {
                'fist_name': 'John',
                'last_name': 'Doe',
                'avatar': file_json_response
            }
        }

        response = self.client.put(
            f'/v1/users/{str(user.id)}',
            json=json_body,
            headers=self.auth_headers()
        )
        assert response.status_code == 200
        found_user = self.users_repository.find_by_id(user.id)
        assert found_user.profile.avatar is not None
        assert found_user.profile.avatar.key == file_json_response['key']
