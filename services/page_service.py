import math
from models import Page
from infrastructure.exceptions import InvalidRequestException


class PageService:
    def get_page(self, paging, page_func, count_func, *args, **kwargs) -> Page:
        paging_errors = self.__validate_paging(paging)
        if paging_errors:
            raise InvalidRequestException(paging_errors)

        skip = (paging.page - 1) * paging.page_size
        limit = paging.page_size
        models = page_func(skip, limit, *args, **kwargs)
        models_count = count_func(*args, **kwargs)
        page_count = math.ceil(models_count / paging.page_size)
        if page_count == 0:
            page_count = 1
        return Page(items=models, page=paging.page, page_count=page_count)

    def __validate_paging(self, paging) -> dict:
        errors = {}
        if paging.page < 1:
            errors["page"] = ["should be greater than zero"]
        if paging.page_size < 1:
            errors["page_size"] = ["should be greater than zero"]
        return errors
