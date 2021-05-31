from ..base_handler import BaseHandler


class ForgotPasswordHandler(BaseHandler):
    def __init__(self, auth_service, response_builder):
        super().__init__(response_builder, None)
        self.auth_service = auth_service

    def handle(self, request, principal=None):
        email = request.json.get('email')
        return self.execute(principal, self.auth_service.request_password_reset, email)
