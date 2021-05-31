from ..base_handler import BaseHandler


class DeleteUserHandler(BaseHandler):
    def __init__(self, users_service, response_builder):
        super().__init__(response_builder, None)
        self.users_service = users_service

    def handle(self, request, user_id, principal=None):
        return self.execute(principal, self.users_service.delete, user_id)
