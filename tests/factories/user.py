from faker import Faker
from bson import ObjectId

from models.translators import (
    UserMongoTranslator,
    TokenPairMongoTranslator,
    PasswordResetRequestMongoTranslator,
    ProfileMongoTranslator
)
from structure import structure


password_service = structure.instantiate('password_service')
precalculated_password_hash = password_service.create_hash('Qq12345!')


class UserFactory:
    def __init__(self):
        self.faker = Faker()
        self.token_pairs_translator = TokenPairMongoTranslator()
        self.password_reset_request_translator = PasswordResetRequestMongoTranslator()
        self.uploaded_file_translator = structure.instantiate('uploaded_file_translator')
        self.profile_translator = ProfileMongoTranslator(
            self.uploaded_file_translator
        )

        self.translator = UserMongoTranslator(
            self.token_pairs_translator,
            self.password_reset_request_translator,
            self.profile_translator,
        )
        self.password_service = structure.instantiate('password_service')

    def generic(self, role, password='Qq12345!'):
        if password == 'Qq12345!':
            password_hash = precalculated_password_hash
        else:
            password_hash = self.password_service.create_hash(password)
        return self.translator.from_document({
            '_id': ObjectId(),
            'email': self.faker.email(),
            'role': role,
            'password_hash': password_hash,
            'token_pairs': [],
            'password_reset_requests': [],
            'profile': {
                'first_name': self.faker.first_name(),
                'last_name': self.faker.last_name(),
                'avatar': None
            }
        })
