from models import (
    User,
    TokenPair,
    PasswordResetRequest,
    UserApplication
)


class UserMongoTranslator:
    def __init__(
            self,
            tokens_pair_translator,
            password_reset_request_translator,
            profile_translator
    ):
        self.tokens_pair_translator = tokens_pair_translator
        self.password_reset_request_translator = password_reset_request_translator
        self.profile_translator = profile_translator

    def to_document(self, user) -> dict:
        token_pairs = [
            self.tokens_pair_translator.to_document(pair)
            for pair in user.token_pairs
        ]
        password_reset_requests = [
            self.password_reset_request_translator.to_document(prr)
            for prr in user.password_reset_requests
        ]
        return {
            '_id': user.id,
            'email': user.email,
            'role': user.role,
            'password_hash': user.password_hash,
            'token_pairs': token_pairs,
            'password_reset_requests': password_reset_requests,
            'profile': self.profile_translator.to_document(user.profile),
            'created_at': user.created_at,
            'last_visit_at': user.last_visit_at
        }

    def from_document(self, document: dict) -> User:
        user = User()
        user.id = document['_id']
        user.email = document['email']
        user.role = document['role']
        user.password_hash = document['password_hash']
        user.token_pairs = [
            self.tokens_pair_translator.from_document(p)
            for p in document['token_pairs']
        ]
        user.password_reset_requests = [
            self.password_reset_request_translator.from_document(prr)
            for prr in document.get('password_reset_requests', [])
        ]
        user.profile = self.profile_translator.from_document(document.get('profile'))
        user.favorite_retailer_ids = document.get('favorite_retailer_ids', [])
        user.created_at = document.get('created_at')
        user.last_visit_at = document.get('last_visit_at')
        return user


class TokenPairMongoTranslator:
    def from_document(self, document) -> TokenPair:
        return TokenPair(
            document.get('id'),
            document.get('access_token'),
            document.get('refresh_token')
        )

    def to_document(self, tokens_pair) -> dict:
        return {
            'id': tokens_pair.id,
            'access_token': tokens_pair.access,
            'refresh_token': tokens_pair.refresh
        }


class PasswordResetRequestMongoTranslator:
    def from_document(self, document) -> PasswordResetRequest:
        result = PasswordResetRequest()
        result.code = document.get('code')
        result.created_at = document.get('created_at')
        return result

    def to_document(self, password_reset_request):
        return {
            'code': password_reset_request.code,
            'created_at': password_reset_request.created_at
        }


class UserApplicationMongoTranslator:
    def __init__(self, profile_translator):
        self.profile_translator = profile_translator

    def from_document(self, document):
        user_application = UserApplication()
        user_application.id = document['_id']
        user_application.email = document['email']
        user_application.role = document['role']
        user_application.password_hash = document['password_hash']
        profile_doc = self.profile_translator.from_document(document.get('profile'))
        user_application.profile = profile_doc
        user_application.code = document.get('code')
        return user_application

    def to_document(self, user_application):
        return {
            '_id': user_application.id,
            'email': user_application.email,
            'role': user_application.role,
            'password_hash': user_application.password_hash,
            'profile': self.profile_translator.to_document(user_application.profile),
            'code': user_application.code
        }
