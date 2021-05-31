from .base_presenter import BasePresenter


class UserPresenter(BasePresenter):
    def __init__(self, profile_presenter):
        self.profile_presenter = profile_presenter

    def present(self, principal, user):
        return {
            'id': str(user.id),
            'email': user.email,
            'role': user.role,
            'profile': self.profile_presenter.present(principal, user.profile),
            'created_at': self.present_time_iso(user.created_at)
        }


class UserApplicationPresenter(BasePresenter):
    def __init__(self, profile_presenter):
        self.profile_presenter = profile_presenter

    def present(self, principal, user):
        return {
            'id': str(user.id),
            'email': user.email,
            'role': user.role,
            'profile': self.profile_presenter.present(principal, user.profile)
        }


class DetailedUserPresenter(BasePresenter):
    def __init__(self, profile_presenter):
        self.profile_presenter = profile_presenter

    def present(self, principal, user):
        return {
            'id': str(user.id),
            'email': user.email,
            'role': user.role,
            'profile': self.profile_presenter.present(principal, user.profile),
            'created_at': self.present_time_iso(user.created_at),
            'last_visit_at': self.present_time_iso(user.last_visit_at)
        }
