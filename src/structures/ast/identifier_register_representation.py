from abc import abstractmethod, ABC


class AbstractIdentifierRegisterRepresentation(ABC):
    @abstractmethod
    def is_numeric(self) -> bool:
        pass

    @abstractmethod
    def get_register(self):
        pass


class IdentifierRegisterRepresentation(AbstractIdentifierRegisterRepresentation):
    def __init__(self, value: int):
        self.value = value

    def get_register(self) -> int:
        return self.value

    def is_numeric(self) -> bool:
        return True


class IdentifierRegisterRepresentation(AbstractIdentifierRegisterRepresentation):
    def __init__(self, generating_str: str):
        self.generating_str = generating_str

    def get_register(self) -> str:
        return self.generating_str

    def is_numeric(self) -> bool:
        return False
