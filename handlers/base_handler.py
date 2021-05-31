from infrastructure.exceptions import (
    InvalidRequestException,
    NotFoundException,
    UnauthorizedException,
    UnauthenticatedException
)


class BaseHandler:
    def __init__(self, response_builder, presenter):
        self.response_builder = response_builder
        self.presenter = presenter

    def execute(self, principal, handler_function, *args, **kwargs):
        try:
            kwargs['principal'] = principal
            result = handler_function(*args, **kwargs)
            response_body = {}
            if isinstance(result, bytes):
                response_body = result
            elif result is not None and self.presenter is not None:
                response_body = self.presenter.present(principal, result)
            response = {"status": 200, "body": response_body}
        except InvalidRequestException as e:
            response = {"status": 400, "body": e.errors}
        except UnauthorizedException:
            response = {
                "status": 403,
                "body": {"message": "access_not_allowed"},
            }
        except NotFoundException:
            response = {"status": 404, "body": {}}
        except UnauthenticatedException:
            response = {"status": 401, "body": {}}
        return self.response_builder.build(response)


class Sorting:
    def __init__(self):
        self.field = None
        self.direction = None

    @staticmethod
    def from_request(request):
        sorting = Sorting()
        sorting.field = request.args.get('sort_field')
        sorting.direction = request.args.get('sort_dir', 'desc').lower()
        return sorting


class ValueFilter:
    def __init__(self, field, value):
        self.field = field
        self.value = value

    @staticmethod
    def extract_list_from_request(request, keys):
        result = []
        request_keys = list(request.args.keys())
        for key in keys:
            if key not in request_keys:
                continue

            result.append(ValueFilter(key, request.args[key]))
        return result


class IntervalFilter:
    def __init__(self, field, value_from, value_to):
        self.field = field
        self.value_from = value_from
        self.value_to = value_to


class Paging:
    def __init__(self):
        self.page = None
        self.page_size = None

    @staticmethod
    def from_request(request):
        def to_int(value, default_value=0) -> int:
            try:
                return int(value)
            except ValueError:
                return default_value
            except TypeError:
                return default_value

        result = Paging()
        result.page = to_int(request.args.get('page'), 1)
        result.page_size = to_int(request.args.get('page_size'), 10)
        return result
