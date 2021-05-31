from ..base_handler import BaseHandler


class GetMeHandler(BaseHandler):
    def __init__(self, users_service, response_builder, presenter):
        super().__init__(response_builder, presenter)
        self.users_service = users_service

    def handle(self, request, principal=None):
        return self.execute(principal, self.users_service.get_principal)
