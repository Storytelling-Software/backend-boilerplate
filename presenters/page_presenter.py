from .base_presenter import BasePresenter


class PagePresenter(BasePresenter):
    def __init__(self, item_presenter):
        self.item_presenter = item_presenter

    def present(self, principal, page):
        return {
            'items': [self.item_presenter.present(principal, item) for item in page.items],
            'page': page.page,
            'page_count': page.page_count,
        }
