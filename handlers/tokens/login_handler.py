from ..base_handler import BaseHandler


class LoginHandler(BaseHandler):
    def __init__(self, auth_service, response_builder, presenter):
        super().__init__(response_builder, presenter)
        self.auth_service = auth_service

    def handle(self, request):
        email = request.json.get('email')
        password = request.json.get('password')
        return self.execute(None, self.auth_service.login, email, password)
