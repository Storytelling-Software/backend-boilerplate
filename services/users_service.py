from models import User, Page, UserApplication

from infrastructure.exceptions import (
    NotFoundException,
    InvalidRequestException,
    UnauthorizedException
)


class UsersService:
    def __init__(
            self, users_repository, user_applications_repository, password_service,
            create_user_validator_service, create_admin_validator_service, update_user_validator_service,
            page_service, email_list_service, user_email_service, user_files_migration_service
    ) -> None:
        self.users_repository = users_repository
        self.user_applications_repository = user_applications_repository
        self.password_service = password_service
        self.create_user_validator_service = \
            create_user_validator_service
        self.create_admin_validator_service = \
            create_admin_validator_service
        self.update_user_validator_service = \
            update_user_validator_service
        self.page_service = page_service
        self.email_list_service = email_list_service
        self.user_email_service = user_email_service
        self.user_files_migration_service = user_files_migration_service

    def create(self, attributes: dict, password_length=8, principal=None) -> UserApplication:
        self.create_user_validator_service.validate(attributes)
        password = attributes.get('password')
        if not password:
            password = self.password_service.generate_password(password_length)
        attributes['password_hash'] = self.password_service.create_hash(password)
        attributes['email'] = attributes['email'].lower()

        application = self.user_applications_repository.find_by_email(attributes['email'])
        if not application:
            application = UserApplication.from_request(attributes)
            application.id = self.user_applications_repository.create(application)
            self.user_email_service.send_account_confirmation(application, application.code)
        else:
            application.assign_request(attributes)
            self.user_applications_repository.update(application)
        return application

    def confirm_registration(self, attributes: dict, principal=None) -> User:
        email = attributes.get('email')
        code = attributes.get('code')
        application = self.user_applications_repository.find_by_email(email)
        if not application or application.code != code:
            error = {
                'code': [
                    {'message': 'Invalid code', 'key': 'error_invalid_code'}
                ]
            }
            raise InvalidRequestException(error)

        user = User.from_application(application)
        user.id = self.users_repository.create(user)
        self.user_applications_repository.delete(application)
        self.email_list_service.add_user(user)

        return user

    def create_admin(self, attributes: dict, password_length=8, principal=None) -> User:
        self.create_admin_validator_service.validate(attributes)
        password = self.password_service.generate_password(password_length)
        attributes['password_hash'] = self.password_service.create_hash(password)
        attributes['email'] = attributes['email'].lower()
        attributes['role'] = 'admin'
        user = User.from_request(attributes)

        user.id = self.users_repository.create(user)
        if user.id:
            self._send_account_details(user, password)
        return user

    def delete(self, user_id: str, principal=None) -> None:
        user = self.__find_user(user_id)
        self.users_repository.delete(user)

    def update(self, user_id: str, attributes: dict, principal=None) -> User:
        self.update_user_validator_service.validate(attributes)
        user = self.__find_user(user_id)
        self.__check_user_authorization(user_id, principal)

        email_collision = self.users_repository.find_by_email(attributes.get('email'))
        if email_collision and str(email_collision.id) != user_id:
            error = {
                'code': [
                    {'message': 'Already taken', 'key': 'error_already_taken'}
                ]
            }
            raise InvalidRequestException(error)

        user.assign_request(attributes)

        files = user.profile.get_files()
        self.user_files_migration_service.migrate(files)
        self.users_repository.update(user)
        return user

    def find(self, user_id: str, principal=None) -> User:
        user = self.__find_user(user_id)
        return user

    def get_page(self, paging, role, principal=None) -> Page:
        return self.page_service.get_page(
            paging,
            self.users_repository.get_page,
            self.users_repository.count,
            role
        )

    def get_list(self, principal=None) -> list:
        return self.users_repository.get_list()

    def find_own(self, principal=None) -> User:
        return self.users_repository.find_by_id(principal.id)

    def get_principal(self, principal=None) -> User:
        return principal

    def search(self, paging, query, role, principal=None) -> Page:
        return self.page_service.get_page(
            paging,
            self.users_repository.search,
            self.users_repository.count_for_search,
            query,
            role
        )

    def resend_user_confirmation(self, attributes, principal=None) -> None:
        email = attributes.get('email')
        application = self.user_applications_repository.find_by_email(email)
        if not application:
            return None
        application.generate_code()
        self.user_applications_repository.update(application)
        self.user_email_service.send_account_confirmation(application, application.code)
        return None

    def _send_account_details(self, user, password) -> None:
        self.user_email_service.send_account_details(user, password)

    def __find_user(self, user_id) -> User:
        user = self.users_repository.find_by_id(user_id)
        if not user:
            raise NotFoundException()
        return user

    def __check_user_authorization(self, user_id, principal) -> None:
        if principal.role == 'user' and str(principal.id) != user_id:
            raise UnauthorizedException()
