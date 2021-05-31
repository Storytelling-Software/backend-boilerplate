from .base_presenter import BasePresenter


class TokenPairPresenter(BasePresenter):
    def present(self, principal, item):
        return {
            'access': item.access,
            'refresh': item.refresh
        }
