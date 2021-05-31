from infrastructure.exceptions import InvalidRequestException


class ValidatorService:
    def __init__(self, validators: list) -> None:
        self.validators = validators

    def validate(self, args: dict) -> None:
        errors = []

        for validator in self.validators:
            if validator.is_valid(args):
                continue
            errors.append({validator.key: validator.error()})

        compressed_errors = {}

        for error in errors:
            key = list(error.keys())[0]
            if key not in compressed_errors:
                compressed_errors[key] = []
            compressed_errors[key].append(error[key])

        if compressed_errors:
            raise InvalidRequestException(compressed_errors)
