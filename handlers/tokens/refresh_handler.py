from ..base_handler import BaseHandler


class RefreshHandler(BaseHandler):
    def __init__(self, auth_service, response_builder, presenters):
        super().__init__(response_builder, presenters)
        self.auth_service = auth_service

    def handle(self, request):
        refresh_token = request.json.get('refresh_token')
        return self.execute(None, self.auth_service.refresh, refresh_token)
