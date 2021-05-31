from ..base_handler import BaseHandler


class ConfirmUserHandler(BaseHandler):
    def __init__(self, users_service, response_builder, presenter):
        super().__init__(response_builder, presenter)
        self.users_service = users_service

    def handle(self, request, principal=None):
        attributes = request.json
        return self.execute(
            principal, 
            self.users_service.confirm_registration, 
            attributes
        )
