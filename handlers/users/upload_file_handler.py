from ..base_handler import BaseHandler


class UploadFileToUserHandler(BaseHandler):
    def __init__(self, s3_wrapper, response_builder, presenter):
        super().__init__(response_builder, presenter)
        self.s3_wrapper = s3_wrapper

    def handle(self, request, principal=None):
        file = request.files.get('file')
        return self.execute(principal, self.s3_wrapper.upload_file, file)
