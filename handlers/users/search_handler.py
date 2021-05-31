from ..base_handler import BaseHandler, Paging


class SearchUsersHandler(BaseHandler):
    def __init__(
            self,
            users_service,
            response_builder,
            presenter
    ):
        super().__init__(response_builder, presenter)
        self.users_service = users_service

    def handle(self, request, principal=None):
        role = request.args.get('role', 'user')
        query = request.args.get('query', '')
        paging = Paging.from_request(request)
        return self.execute(principal, self.users_service.search, paging, query, role)
