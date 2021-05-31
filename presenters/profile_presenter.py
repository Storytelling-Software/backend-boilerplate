from .base_presenter import BasePresenter


class ProfilePresenter(BasePresenter):
    def __init__(self, uploaded_file_presenter):
        self.uploaded_file_presenter = uploaded_file_presenter

    def present(self, principal, user_profile):
        return {
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'avatar': self.uploaded_file_presenter.present(
                principal, user_profile.avatar
            )
        }
