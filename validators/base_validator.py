from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @abstractmethod
    def is_valid(self, args) -> None:
        pass

    @abstractmethod
    def error(self) -> None:
        pass


class BaseKeyValidator(BaseValidator):
    def __init__(self, key: str) -> None:
        self.key = key
