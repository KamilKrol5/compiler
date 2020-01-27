from typing import Tuple


class CompilationException(Exception):
    def __init__(self, message: str, occurrence_place: Tuple[int, int] = (0, 0)):
        super().__init__(message)
        self.occurrence_place: Tuple[int, int] = occurrence_place


class LocalVariableAlreadyDeclaredException(Exception):
    pass


class AnAttemptToRemoveNonExistingLocalVariable(Exception):
    pass


class UndeclaredVariableException(CompilationException):
    pass


class UndeclaredArrayException(CompilationException):
    pass


class AnAttemptToModifyCounterException(CompilationException):
    pass


class MultipleDeclarationException(CompilationException):
    pass


class ArrayEndSmallerThanStartException(CompilationException):
    pass
