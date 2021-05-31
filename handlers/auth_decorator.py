from infrastructure.exceptions import UnauthenticatedException, UnauthorizedException
from datetime import datetime


class Auth:
    def __init__(self, roles, allow_anonymous):
        self.roles = roles
        self.allow_anonymous = allow_anonymous


class AuthFactory:
    def strict(self, roles):
        return Auth(roles, False)

    def liberal(self):
        return Auth('*', True)


class AuthDecoratorFactory:
    def __init__(self, auth_service, response_builder, celery):
        self.auth_service = auth_service
        self.response_builder = response_builder
        self.celery = celery

    def decorate(self, handler, policy):
        return AuthDecorator(self.auth_service, self.response_builder, self.celery, policy, handler)


class AuthDecorator:
    def __init__(self, auth_service, response_builder, celery, policy, decoratee):
        self.auth_service = auth_service
        self.response_builder = response_builder
        self.celery = celery
        self.policy = policy
        self.decoratee = decoratee

    def handle(self, request, *args, principal=None):
        auth_header = request.headers.get('Authorization')
        user = None
        try:
            user = self.auth_service.authenticate(
                auth_header, self.policy.allow_anonymous)
            self.auth_service.authorize(user, self.policy.roles)
        except UnauthenticatedException:
            response = {"status": 401, "body": {}}
            return self.response_builder.build(response)
        except UnauthorizedException:
            response = {
                "status": 403,
                "body": {
                    "message": "access_not_allowed"
                }
            }
            return self.response_builder.build(response)
        if user:
            self.celery.send_task(
                'background_jobs.update_last_visit',
                [str(user.id), datetime.utcnow().timestamp()]
            )
        return self.decoratee.handle(request, *args, principal=user)
