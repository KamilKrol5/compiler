from abc import abstractmethod, ABC


class AbstractIdentifierAccess(ABC):
    @abstractmethod
    def store(self):
        pass

    @abstractmethod
    def prepare_register(self):
        pass

    @abstractmethod
    def load(self):
        pass


class StaticIdentifierAccess(AbstractIdentifierAccess):

    def __init__(self, value: int):
        self.value = value

    def load(self):
        return f'LOAD {self.value}\n'

    def store(self) -> str:
        return f'STORE {self.value}\n'

    def prepare_register(self) -> str:
        return ""


class DynamicIdentifierAccess(AbstractIdentifierAccess):

    def __init__(self, generating_str: str):
        self.generating_str = generating_str

    def load(self):
        return f'LOADI {9}\n'

    def store(self) -> str:
        return "STOREI 9\n"

    def prepare_register(self):
        return self.generating_str + "STORE 9\n"
