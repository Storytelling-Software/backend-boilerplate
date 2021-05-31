from types import LambdaType
import string
from mock import Mock
from builders import ResponseBuilder

from dependencies import Dependencies

from wrappers import BcryptWrapper, S3Wrapper

from repositories import (
    UsersRepository,
    UserApplicationsRepository
)

from models import PasswordGenerator, PasswordPartGenerator

from handlers import (
    ResetPasswordHandler,
    ChangePasswordHandler,
    ForgotPasswordHandler,
    LoginHandler,
    LogoutHandler,
    RefreshHandler,
    CreateUserHandler,
    GetUsersPageHandler,
    GetMeHandler,
    SearchUsersHandler,
    CreateAdminHandler,
    GetUserHandler,
    UpdateUserHandler,
    DeleteUserHandler,
    ConfirmUserHandler,
    ResendUserConfirmationHandler,
    UploadFileToUserHandler,
    SendEnquiryHandler,
)

from services import (
    UsersService,
    PasswordService,
    ValidatorService,
    TokensService,
    AuthService,
    PageService,
    EmailListService,
    UserEmailService,
    EmailSendingService,
    FileMigrationService,
    EnquiryEmailService,
)

from models.translators import (
    UserMongoTranslator,
    TokenPairMongoTranslator,
    PasswordResetRequestMongoTranslator,
    ProfileMongoTranslator,
    UploadedFileMongoTranslator,
    UserApplicationMongoTranslator,
)

from validators import (
    EmailRegexValidator,
    EmailUniqueValidator,
    LengthValidator,
    PresenceValidator,
    IdValidator,
    IdListValidator,
    NameUniqueValidator,
    NumericValidator,
    ListTypeValidator,
    UserIdValidator,
    StringDateValidator,
    PresenceNumericValidator,
    IntegerValidator,
    DictionaryValidator,
    PositiveValidator,
    NegativeValidator,
)

from presenters import (
    TokenPairPresenter,
    UserPresenter,
    DetailedUserPresenter,
    ProfilePresenter,
    PagePresenter,
    UploadedFilePresenter,
    UserApplicationPresenter,
)

from handlers.auth_decorator import AuthFactory, AuthDecoratorFactory
from models.factories.mongo_index_factory import MongoIndexFactory, MongoColumnFactory

auth_factory = AuthFactory()
index_factory = MongoIndexFactory()
column_factory = MongoColumnFactory()


class Structure:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies
        self.structure = {
            'response_builder': {
                'class': ResponseBuilder,
                'args': []
            },
            'bcrypt_wrapper': {
                'class': BcryptWrapper,
                'args': []
            },
            'auth_decorator_factory': {
                'class': AuthDecoratorFactory,
                'args': [
                    'auth_service',
                    'response_builder',
                    lambda: deps.celery(),
                ]
            },
            'users_repository': {
                'class': UsersRepository,
                'args': [
                    lambda: self.dependencies.pymongo_wrapper().get_collection(
                        self.dependencies.mongo(), 'users'),
                    'user_mongo_translator',
                    lambda: []
                ]
            },
            'user_applications_repository': {
                'class': UserApplicationsRepository,
                'args': [
                    lambda: self.dependencies.pymongo_wrapper().get_collection(
                        self.dependencies.mongo(), 'user_applications'),
                    'user_application_mongo_translator',
                    lambda: []
                ]
            },
            'profile_mongo_translator': {
                'class': ProfileMongoTranslator,
                'args': [
                    'uploaded_file_translator'
                ]
            },
            'user_mongo_translator': {
                'class': UserMongoTranslator,
                'args': [
                    'tokens_pair_mongo_translator',
                    'password_reset_request_mongo_translator',
                    'profile_mongo_translator'
                ]
            },
            'user_application_mongo_translator': {
                'class': UserApplicationMongoTranslator,
                'args': [
                    'profile_mongo_translator'
                ]
            },
            'tokens_pair_mongo_translator': {
                'class': TokenPairMongoTranslator,
                'args': []
            },
            'password_reset_request_mongo_translator': {
                'class': PasswordResetRequestMongoTranslator,
                'args': []
            },
            'digits_generator': {
                'class': PasswordPartGenerator,
                'args': [
                    lambda: string.digits
                ]
            },
            'lower_letters_generator': {
                'class': PasswordPartGenerator,
                'args': [
                    lambda: string.ascii_lowercase
                ]
            },
            'upper_letters_generator': {
                'class': PasswordPartGenerator,
                'args': [
                    lambda: string.ascii_uppercase
                ]
            },
            'password_generator': {
                'class': PasswordGenerator,
                'args': [
                    [
                        'digits_generator',
                        'lower_letters_generator',
                        'upper_letters_generator'
                    ]
                ]
            },
            'password_service': {
                'class': PasswordService,
                'args': [
                    'bcrypt_wrapper',
                    'password_generator'
                ]
            },
            'email_presence_validator': {
                'class': PresenceValidator,
                'args': [
                    lambda: 'email'
                ]
            },
            'email_regex_validator': {
                'class': EmailRegexValidator,
                'args': [
                    lambda: 'email'
                ]
            },
            'email_unique_validator': {
                'class': EmailUniqueValidator,
                'args': [
                    lambda: 'email',
                    'users_repository'
                ]
            },
            'password_presence_validator': {
                'class': PresenceValidator,
                'args': [
                    lambda: 'password'
                ]
            },
            'password_length_validator': {
                'class': LengthValidator,
                'args': [
                    lambda: 'password',
                    lambda: 6,
                    lambda: 256
                ]
            },
            'phone_number_presence_validator': {
                'class': PresenceValidator,
                'args': [
                    lambda: 'phone_number'
                ]
            },
            'phone_number_length_validator': {
                'class': LengthValidator,
                'args': [
                    lambda: 'phone_number',
                    lambda: 5,
                    lambda: 15
                ]
            },
            'name_presence_validator': {
                'class': PresenceValidator,
                'args': [
                    lambda: 'name'
                ]
            },
            'timeline_numeric_validator': {
                'class': NumericValidator,
                'args': [
                    lambda: 'timeline'
                ]
            },
            'user_create_validator_service': {
                'class': ValidatorService,
                'args': [
                    [
                        'email_presence_validator',
                        'email_regex_validator',
                        'email_unique_validator',
                        'password_presence_validator',
                        'password_length_validator'
                    ]
                ]
            },
            'admin_create_validator_service': {
                'class': ValidatorService,
                'args': [
                    [
                        'email_presence_validator',
                        'email_regex_validator',
                        'email_unique_validator'
                    ]
                ]
            },
            'user_update_validator_service': {
                'class': ValidatorService,
                'args': [
                    [
                        'email_presence_validator',
                        'email_regex_validator'
                    ]
                ]
            },
            'tokens_service': {
                'class': TokensService,
                'args': [
                    lambda: deps.environment_wrapper().get_var('JWT_SECRET'),
                    lambda: int(deps.environment_wrapper().get_var(
                        'JWT_ACCESS_TTL_MINUTES')),
                    lambda: int(deps.environment_wrapper().get_var(
                        'JWT_REFRESH_TTL_HOURS'))
                ]
            },
            'users_service': {
                'class': UsersService,
                'args': [
                    'users_repository',
                    'user_applications_repository',
                    'password_service',
                    'user_create_validator_service',
                    'admin_create_validator_service',
                    'user_update_validator_service',
                    'page_service',
                    'email_list_service_mocking',
                    'user_email_service',
                    'user_file_migration_service'
                ]
            },
            'auth_service': {
                'class': AuthService,
                'args': [
                    'users_repository',
                    'password_service',
                    'tokens_service',
                    'user_email_service',
                    'password_reset_validation_service',
                    'password_change_validation_service'
                ]
            },
            'reset_password_handler': {
                'class': ResetPasswordHandler,
                'args': [
                    'auth_service',
                    'response_builder'
                ]
            },
            'new_password_length_validator': {
                'class': LengthValidator,
                'args': [
                    lambda: 'new_password',
                    lambda: 6,
                    lambda: 32
                ]
            },
            'password_reset_validation_service': {
                'class': ValidatorService,
                'args': [
                    [
                        'new_password_length_validator'
                    ]
                ]
            },
            'password_change_validation_service': {
                'class': ValidatorService,
                'args': [
                    [
                        'new_password_length_validator'
                    ]
                ]
            },
            'change_password_handler': {
                'class': ChangePasswordHandler,
                'args': [
                    'auth_service',
                    'response_builder',
                    'tokens_presenter'
                ]
            },
            'change_password_auth_handler':
                lambda: self.decorate_auth_handler(
                    'change_password_handler',
                    auth_factory.strict('*')
                ),
            'tokens_presenter': {
                'class': TokenPairPresenter,
                'args': []
            },
            'forgot_password_handler': {
                'class': ForgotPasswordHandler,
                'args': [
                    'auth_service',
                    'response_builder'
                ]
            },
            'logout_handler': {
                'class': LogoutHandler,
                'args': [
                    'auth_service',
                    'response_builder'
                ]
            },
            'logout_auth_handler':
                lambda: self.decorate_auth_handler(
                    'logout_handler',
                    auth_factory.strict('*')
                ),
            'refresh_handler': {
                'class': RefreshHandler,
                'args': [
                    'auth_service',
                    'response_builder',
                    'tokens_presenter'
                ]
            },
            'login_handler': {
                'class': LoginHandler,
                'args': [
                    'auth_service',
                    'response_builder',
                    'tokens_presenter'
                ]
            },
            'page_service': {
                'class': PageService,
                'args': []
            },
            'create_user_handler': {
                'class': CreateUserHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'user_application_presenter'
                ]
            },
            'create_user_auth_handler':
                lambda: self.decorate_auth_handler(
                    'create_user_handler',
                    auth_factory.liberal()
                ),
            'user_presenter': {
                'class': UserPresenter,
                'args': [
                    'profile_presenter'
                ]
            },
            'detailed_user_presenter': {
                'class': UserPresenter,
                'args': [
                    'profile_presenter'
                ]
            },
            'user_application_presenter': {
                'class': UserApplicationPresenter,
                'args': [
                    'profile_presenter'
                ]
            },
            'profile_presenter': {
                'class': ProfilePresenter,
                'args': [
                    'user_file_presenter'
                ]
            },
            'create_admin_handler': {
                'class': CreateAdminHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'user_presenter'
                ]
            },
            'create_admin_auth_handler':
                lambda: self.decorate_auth_handler(
                    'create_admin_handler',
                    auth_factory.strict(['admin'])
                ),
            'get_user_handler': {
                'class': GetUserHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'detailed_user_presenter'
                ]
            },
            'get_user_auth_handler':
                lambda: self.decorate_auth_handler(
                    'get_user_handler',
                    auth_factory.strict(['admin'])
                ),
            'update_user_handler': {
                'class': UpdateUserHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'user_presenter'
                ]
            },
            'update_user_auth_handler':
                lambda: self.decorate_auth_handler(
                    'update_user_handler',
                    auth_factory.strict(['admin', 'user'])
                ),
            'delete_user_handler': {
                'class': DeleteUserHandler,
                'args': [
                    'users_service',
                    'response_builder'
                ]
            },
            'delete_user_auth_handler':
                lambda: self.decorate_auth_handler(
                    'delete_user_handler',
                    auth_factory.strict(['admin'])
                ),
            'uploaded_file_translator': {
                'class': UploadedFileMongoTranslator,
                'args': []
            },
            'get_users_page_handler': {
                'class': GetUsersPageHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'users_page_presenter'
                ]
            },
            'get_users_page_auth_handler':
                lambda: self.decorate_auth_handler(
                    'get_users_page_handler',
                    auth_factory.strict(['admin'])
                ),
            'users_page_presenter': {
                'class': PagePresenter,
                'args': [
                    'user_presenter'
                ]
            },
            'get_me_handler': {
                'class': GetMeHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'user_presenter',
                ]
            },
            'get_me_auth_handler':
                lambda: self.decorate_auth_handler(
                    'get_me_handler',
                    auth_factory.strict('*')
                ),
            'user_email_service': {
                'class': UserEmailService,
                'args': [
                    lambda: deps.celery(),
                    lambda: deps.environment_wrapper().get_var('MANDRILL_NOREPLY_EMAIL'),
                ]
            },
            'email_sending_service': {
                'class': EmailSendingService,
                'args': [
                    lambda: deps.mandrill()
                ]
            },
            'email_list_service': {
                'class': EmailListService,
                'args': [
                    lambda: deps.mailchimp(),
                    lambda: deps.environment_wrapper().get_var('MAILCHIMP_LIST_ID'),
                ]
            },
            'email_list_service_mocking': {
                'class': EmailListService,
                'args': [
                    lambda: Mock(),
                    lambda: Mock(),
                ]
            },
            'search_users_handler': {
                'class': SearchUsersHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'users_page_presenter'
                ]
            },
            'search_users_auth_handler':
                lambda: self.decorate_auth_handler(
                    'search_users_handler',
                    auth_factory.strict(['admin'])
                ),
            'user_id_validator': {
                'class': IdValidator,
                'args': [
                    lambda: 'user_id'
                ]
            },
            'confirm_user_handler': {
                'class': ConfirmUserHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'user_presenter'
                ]
            },
            'resend_user_confirmation_handler': {
                'class': ResendUserConfirmationHandler,
                'args': [
                    'users_service',
                    'response_builder',
                    'user_presenter'
                ]
            },
            'user_file_presenter': {
                'class': UploadedFilePresenter,
                'args': [
                    'user_file_s3_wrapper'
                ]
            },
            'user_temp_file_presenter': {
                'class': UploadedFilePresenter,
                'args': [
                    'user_temp_file_s3_wrapper'
                ]
            },
            'user_file_s3_wrapper': {
                'class': S3Wrapper,
                'args': [
                    lambda: deps.s3_client(),
                    lambda: deps.environment_wrapper().get_var('S3_BUCKET_NAME'),
                    lambda: 'users_files/'
                ]
            },
            'user_temp_file_s3_wrapper': {
                'class': S3Wrapper,
                'args': [
                    lambda: deps.s3_client(),
                    lambda: deps.environment_wrapper().get_var('S3_TEMP_BUCKET_NAME'),
                    lambda: 'users_files/'
                ]
            },
            'upload_user_file_handler': {
                'class': UploadFileToUserHandler,
                'args': [
                    'user_temp_file_s3_wrapper',
                    'response_builder',
                    'user_temp_file_presenter'
                ]
            },
            'upload_user_file_auth_handler':
                lambda: self.decorate_auth_handler(
                    'upload_user_file_handler',
                    auth_factory.strict('*')
                ),
            'user_file_migration_service': {
                'class': FileMigrationService,
                'args': [
                    lambda: deps.s3_resource(),
                    'user_file_s3_wrapper',
                    'user_temp_file_s3_wrapper'
                ]
            },
            'user_id_presence_validator': {
                'class': PresenceValidator,
                'args': [
                    lambda: 'user_id'
                ]
            },
            'send_enquiry_handler': {
                'class': SendEnquiryHandler,
                'args': [
                    'enquiry_email_service',
                    'response_builder'
                ]
            },
            'send_enquiry_auth_handler':
                lambda: self.decorate_auth_handler(
                    'send_enquiry_handler',
                    auth_factory.liberal()
                ),
            'enquiry_email_service': {
                'class': EnquiryEmailService,
                'args': [
                    lambda: deps.celery(),
                    lambda: deps.environment_wrapper().get_var('MANDRILL_NOREPLY_EMAIL'),
                    lambda: deps.environment_wrapper().get_var('ENQUIRY_CONTACT_EMAIL'),
                ]
            },
        }

    def decorate_auth_handler(self, handler_key, policy):
        factory = self.instantiate('auth_decorator_factory')
        handler = self.instantiate(handler_key)
        return factory.decorate(handler, policy)

    def instantiate(self, key):
        if hasattr(self, key):
            return getattr(self, key)

        element = self.structure[key]
        result = None

        if isinstance(element, dict):
            args = [self.__instantiate_arg(arg) for arg in element.get('args', [])]
            kwargs = {}
            for key in element.get('kwargs', {}):
                kwargs[key] = self.__instantiate_arg(element['kwargs'][key])
            result = element['class'](*args, **kwargs)
        elif isinstance(element, LambdaType):
            result = element()

        setattr(self, key, result)

        return getattr(self, key)

    def __instantiate_arg(self, arg):
        if isinstance(arg, str):
            return self.instantiate(arg)
        elif isinstance(arg, LambdaType):
            return arg()
        elif isinstance(arg, list):
            return [self.instantiate(k) for k in arg]
        elif isinstance(arg, dict):
            value = {}
            for k in arg:
                value[k] = self.instantiate(arg[k])
            return value
        return None


deps = Dependencies()
structure = Structure(deps)
