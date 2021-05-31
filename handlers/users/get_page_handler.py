from ..base_handler import BaseHandler, Paging


class GetUsersPageHandler(BaseHandler):
    def __init__(
            self,
            users_service,
            response_builder,
            presenter
    ):
        super().__init__(response_builder, presenter)
        self.users_service = users_service

    def handle(self, request, principal=None):
        role = request.args.get('role')
        paging = Paging.from_request(request)
        return self.execute(principal, self.users_service.get_page, paging, role)
