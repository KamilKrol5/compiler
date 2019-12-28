from structures.ast.AST import *
from typing import Dict, Tuple

from utils.IO_utils import generate_code_for_write_command, generate_code_for_read_command
from utils.command_utils import generate_code_for_if_then_command
from utils.label_provider import LabelProvider

class ASTInterpreter:
    VARIABLES_START_REGISTER = 100

    def __init__(self, program: Program):
        self.program: Program = program
        self.declared_variables: Dict[str, int] = dict()
        self.declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]] = dict()
        self._assign_registers_to_variables()

    def _assign_registers_to_variables(self):
        # assign registers to variables
        # TODO this can be optimized by shifting array indexes at the end
        for declaration in self.program.declarations.declarations:
            if isinstance(declaration, NumberDeclaration):
                self.declared_variables[declaration.identifier] = self.VARIABLES_START_REGISTER + 1
            elif isinstance(declaration, ArrayDeclaration):
                array_length = declaration.end_index.value - declaration.begin_index.value
                real_start = self.VARIABLES_START_REGISTER + 1
                real_end = self.VARIABLES_START_REGISTER + 1 + array_length

                self.declared_variables[declaration.identifier] = real_start
                self.declared_arrays[declaration.identifier] = (real_start, real_end, declaration)

                self.VARIABLES_START_REGISTER = self.VARIABLES_START_REGISTER + array_length

            self.VARIABLES_START_REGISTER = self.VARIABLES_START_REGISTER + 1
        print(self.VARIABLES_START_REGISTER)
