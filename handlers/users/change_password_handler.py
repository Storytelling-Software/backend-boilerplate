from ..base_handler import BaseHandler


class ChangePasswordHandler(BaseHandler):
    def __init__(self, auth_service, response_builder, tokens_presenter):
        super().__init__(response_builder, tokens_presenter)
        self.auth_service = auth_service

    def handle(self, request, user_id, principal=None):
        auth_header = request.headers.get('Authorization')
        return self.execute(principal, self.auth_service.change_password, user_id, auth_header, request.json)
