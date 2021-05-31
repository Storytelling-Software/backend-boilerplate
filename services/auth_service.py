from bson import ObjectId
from infrastructure.exceptions import UnauthenticatedException, UnauthorizedException, InvalidRequestException
from models import TokenPair, PasswordResetRequest, User
from datetime import datetime, timedelta


class AuthService:
    def __init__(self, users_repository, password_service, tokens_service, user_email_service,
                 password_reset_validation_service, password_change_validation_service) -> None:
        self.users_repository = users_repository
        self.password_service = password_service
        self.tokens_service = tokens_service
        self.user_email_service = user_email_service
        self.password_reset_validation_service = password_reset_validation_service
        self.password_change_validation_service = password_change_validation_service

    def login(self, email, password, principal=None) -> TokenPair:
        user = self.users_repository.find_by_email(email)
        if not user:
            raise UnauthenticatedException()

        if not self.password_service.check(password, user.password_hash):
            raise UnauthenticatedException()

        new_pair = self.__create_pair(user)

        user.token_pairs.append(new_pair)
        self.users_repository.update(user)
        return new_pair

    def refresh(self, refresh_token, principal=None) -> TokenPair:
        refresh_payload = self.__get_payload(refresh_token)
        user = self.__get_user_by_token(refresh_payload)

        pair_id = refresh_payload.get('id')
        refreshed_pairs = [p for p in user.token_pairs if str(p.id) == pair_id]
        if not refreshed_pairs or len(refreshed_pairs) == 0:
            raise UnauthenticatedException()

        pair = refreshed_pairs[0]
        if self.tokens_service.decode(pair.access):
            return pair

        new_pair = self.__create_pair(user, refresh_token, pair_id)
        user.token_pairs = self.__remove_token_pairs(user, pair_id)
        user.token_pairs.append(new_pair)
        self.users_repository.update(user)
        return new_pair

    def logout(self, auth_header, principal=None) -> None:
        token = self.__get_token_from_header(auth_header)
        payload = self.__get_payload(token)
        user = self.__get_user_by_token(payload)

        pair_id = payload.get('id')
        user.token_pairs = self.__remove_token_pairs(user, pair_id)

        self.users_repository.update(user)

    def authenticate(self, auth_header, allow_anonymous) -> User or None:
        jwt = self.__get_token_from_header(auth_header, allow_anonymous)
        if not jwt:
            if allow_anonymous:
                return None
            else:
                raise UnauthenticatedException()
        payload = self.__get_payload(jwt)
        user = self.__get_user_by_token(payload, allow_anonymous)

        access_tokens = list(
            map(lambda pair: pair.access, user.token_pairs))

        if jwt not in access_tokens:
            if allow_anonymous:
                return None
            else:
                raise UnauthenticatedException()
        return user

    def authorize(self, user, roles) -> None:
        role = None
        if user:
            role = user.role
        if roles != '*' and role not in roles:
            raise UnauthorizedException()

    def request_password_reset(self, email, principal=None) -> None:
        user = self.users_repository.find_by_email(email)
        if not user:
            return

        reset_request = PasswordResetRequest()
        user.password_reset_requests = [reset_request]
        self.users_repository.update(user)
        self.user_email_service.recover_password(user, reset_request.code)

    def reset_password(self, params, principal=None) -> None:
        user = self.users_repository.find_password_reset(params.get('code'))
        if not user or params.get('email') != user.email:
            error = {
                'code': [
                    {'message': 'Invalid code', 'key': 'error_invalid_code'}
                ]
            }
            raise InvalidRequestException(error)
        password_reset_request = [
            prr for prr in user.password_reset_requests if prr.code == params.get('code')
        ][0]
        expires_at = password_reset_request.created_at + timedelta(hours=24)
        if datetime.utcnow() > expires_at:
            error = {
                'code': [
                    {'message': 'Invalid code', 'key': 'error_invalid_code'}
                ]
            }
            raise InvalidRequestException(error)

        self.password_reset_validation_service.validate(params)
        user.password_hash = self.password_service.create_hash(params['new_password'])
        user.token_pairs = []
        user.password_reset_requests = []
        self.users_repository.update(user)

    def change_password(self, user_id, auth_header, params, principal=None) -> TokenPair:
        if str(principal.id) != user_id:
            raise UnauthorizedException()
        principal = self.authenticate(auth_header, False)
        self.password_change_validation_service.validate(params)
        old_password = params.get('old_password')
        if not self.password_service.check(old_password, principal.password_hash):
            error = {
                'old_password': [
                    {'message': 'Invalid password', 'key': 'error_invalid_password'}
                ]
            }
            raise InvalidRequestException(error)
        principal.password_hash = self.password_service.create_hash(params['new_password'])
        principal.token_pairs = []
        principal.password_reset_requests = []
        self.users_repository.update(principal)
        return self.login(principal.email, params['new_password'])

    def __create_pair(self, user, refresh_token=None, token_id=None) -> TokenPair:
        if not token_id:
            token_id = ObjectId()
        claims = {
            'id': str(token_id),
            'user_id': str(user.id),
            'role': user.role
        }
        access = self.tokens_service.encode('access', claims)
        if not refresh_token:
            refresh_token = self.tokens_service.encode('refresh', claims)
        return TokenPair(token_id, access, refresh_token)

    def __get_user_by_token(self, payload, allow_anonymous=None) -> User or None:
        user_id = payload.get('user_id')
        user = self.users_repository.find_by_id(user_id)

        if not user:
            if allow_anonymous:
                return None
            else:
                raise UnauthenticatedException()

        return user

    def __get_token_from_header(self, auth_header, allow_anonymous=None) -> None or str:
        if not auth_header:
            if allow_anonymous:
                return None
            raise UnauthenticatedException()
        authorization = auth_header.split(" ")
        if len(authorization) != 2 or authorization[0].lower() != "token":
            if allow_anonymous:
                return None
            raise UnauthenticatedException()
        token = authorization[1]

        return token

    def __get_payload(self, token) -> dict:
        payload = self.tokens_service.decode(token)
        if not payload:
            raise UnauthenticatedException()

        return payload

    def __remove_token_pairs(self, user, pair_id) -> list:
        user.token_pairs = [
            p for p in user.token_pairs if str(p.id) != str(pair_id)]

        return user.token_pairs
