from datetime import datetime
from random import choice, randint
from string import ascii_uppercase
from .profile import Profile


class User:
    def __init__(self) -> None:
        self.id = None
        self.email = None
        self.role = None
        self.password_hash = None
        self.token_pairs = None
        self.password_reset_requests = None
        self.profile = None
        self.favorite_retailer_ids = None
        self.created_at = None
        self.last_visit_at = None

    @staticmethod
    def from_request(attributes: dict):
        user = User()
        user.email = attributes['email']
        user.role = attributes.get('role', 'user')
        user.password_hash = attributes['password_hash']
        user.token_pairs = []
        user.password_reset_requests = []
        user.profile = Profile.from_request(attributes.get('profile', {}))
        user.favorite_retailer_ids = []
        user.created_at = datetime.utcnow()
        return user

    @staticmethod
    def from_application(application):
        user = User()
        user.id = application.id
        user.email = application.email
        user.role = application.role
        user.password_hash = application.password_hash
        user.profile = application.profile
        user.token_pairs = []
        user.password_reset_requests = []
        user.favorite_retailer_ids = []
        user.created_at = datetime.utcnow()
        return user

    def assign_request(self, attributes: dict) -> None:
        self.email = attributes['email']
        self.profile.assign_request(attributes.get('profile', {}))


class TokenPair:
    def __init__(self, token_pair_id, access, refresh):
        self.id = token_pair_id
        self.access = access
        self.refresh = refresh


class PasswordResetRequest:
    def __init__(self) -> None:
        self.code = ''.join(choice(ascii_uppercase) for i in range(6))
        self.created_at = datetime.utcnow()


class UserApplication:
    def __init__(self):
        self.id = None
        self.email = None
        self.role = None
        self.password_hash = None
        self.profile = None
        self.code = None

    @staticmethod
    def from_request(attributes: dict):
        application = UserApplication()
        application.email = attributes['email']
        application.role = attributes.get('role', 'user')
        application.password_hash = attributes['password_hash']
        application.profile = Profile.from_request(attributes.get('profile', {}))
        application.code = ''.join([str(randint(0, 9)) for _ in range(6)])
        return application

    def generate_code(self):
        self.code = ''.join([str(randint(0, 9)) for _ in range(6)])

    def assign_request(self, attributes):
        self.email = attributes['email']
        self.role = attributes.get('role', 'user')
        self.password_hash = attributes['password_hash']
        self.profile = Profile.from_request(attributes.get('profile', {}))
