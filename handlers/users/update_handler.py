from ..base_handler import BaseHandler


class UpdateUserHandler(BaseHandler):
    def __init__(self, users_service, response_builder, presenter):
        super().__init__(response_builder, presenter)
        self.users_service = users_service

    def handle(self, request, user_id, principal=None):
        attributes = request.json
        return self.execute(principal, self.users_service.update, user_id, attributes)
