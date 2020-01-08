from abc import abstractmethod, ABC


class IdentifierRegisterRepresentationAbstract(ABC):
    @abstractmethod
    def is_numeric(self) -> bool:
        pass

    @abstractmethod
    def get_register(self):
        pass


class IdentifierRegisterPureNumberRepresentation(IdentifierRegisterRepresentationAbstract):
    def __init__(self, value: int):
        self.value = value

    def get_register(self) -> int:
        return self.value

    def is_numeric(self) -> bool:
        return True


class IdentifierRegisterGeneratingStringRepresentation(IdentifierRegisterRepresentationAbstract):
    def __init__(self, generating_str: str):
        self.generating_str = generating_str

    def get_register(self) -> str:
        return self.generating_str

    def is_numeric(self) -> bool:
        return False
