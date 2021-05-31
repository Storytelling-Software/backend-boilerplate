from .base_presenter import BasePresenter


class UploadedFilePresenter(BasePresenter):
    def __init__(self, s3_wrapper):
        self.s3_wrapper = s3_wrapper

    def present(self, principal, uploaded_file):
        if not uploaded_file:
            return None
        return {
            'key': uploaded_file.key,
            'link': self.s3_wrapper.link(uploaded_file.key),
            'filename': uploaded_file.filename
        }
