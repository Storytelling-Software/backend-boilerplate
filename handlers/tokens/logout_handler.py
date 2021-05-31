from ..base_handler import BaseHandler


class LogoutHandler(BaseHandler):
    def __init__(self, auth_service, response_builder):
        super().__init__(response_builder, None)
        self.auth_service = auth_service

    def handle(self, request, principal=None):
        auth_header = request.headers.get("authorization", "")
        return self.execute(auth_header, self.auth_service.logout, auth_header)
