from ..base_handler import BaseHandler


class ResetPasswordHandler(BaseHandler):
    def __init__(self, auth_service, response_builder):
        super().__init__(response_builder, None)
        self.auth_service = auth_service

    def handle(self, request):
        params = request.json
        return self.execute(None, self.auth_service.reset_password, params)
