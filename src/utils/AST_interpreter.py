from structures.ast.AST import *
from typing import Dict, Tuple

from utils.IO_utils import generate_code_for_write_command, generate_code_for_read_command
from utils.command_utils import write_code_for_if_then_command, write_code_for_if_then_else_command, \
    write_code_for_assignment_command
from utils.expression_utils import generate_code_for_expression
from utils.label_provider import LabelProvider
from utils.loop_utils import generate_condition


class ASTInterpreter(Visitor):
    VARIABLES_START_REGISTER = 100

    def __init__(self, program: Program):
        self.program: Program = program
        self.declared_variables: Dict[str, int] = dict()
        self.declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]] = dict()
        self.generated_code: List[str] = ['## Program\n']
        self.label_provider: LabelProvider = LabelProvider('#label ')
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

    def visit_int_number_value(self, int_number_value: 'IntNumberValue') -> int:
        pass

    def visit_identifier_value(self, identifier_value: 'IdentifierValue') -> int:
        pass

    def visit_array_element_by_variable_identifier(
            self,
            array_element_by_variable_identifier: 'ArrayElementByVariableIdentifier'
    ) -> None:
        pass

    def visit_array_element_by_int_number_identifier(
            self,
            array_element_by_int_number_identifier: 'ArrayElementByIntNumberIdentifier'
    ) -> None:
        pass

    def visit_variable_identifier(self, variable_identifier: 'VariableIdentifier') -> None:
        pass

    def visit_number_declaration(self, number_declaration: 'NumberDeclaration') -> None:
        pass

    def visit_array_declaration(self, array_declaration: 'ArrayDeclaration') -> None:
        pass

    def visit_declarations(self, declarations: 'Declarations') -> None:
        pass

    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue'):
        self.generated_code.append(
            generate_code_for_expression(expression, self.declared_variables, self.declared_arrays))

    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues'):
        self.generated_code.append(
            generate_code_for_expression(expression, self.declared_variables, self.declared_arrays))

    def visit_two_value_condition(self, condition: 'TwoValueCondition'):
        # TODO change it
        self.generated_code.append(
            generate_condition(condition, self.declared_variables, self.declared_arrays))

    def visit_commands(self, commands: 'Commands') -> None:
        for c in commands.commands:
            c.accept(self)

    def visit_assignment_command(self, assignment_command: 'AssignmentCommand') -> None:
        write_code_for_assignment_command(assignment_command, self)

    def visit_if_then_else_command(self, if_then_else_command: 'IfThenElseCommand') -> None:
        write_code_for_if_then_else_command(if_then_else_command, self)

    def visit_if_then_command(self, if_then_command: 'IfThenCommand') -> None:
        write_code_for_if_then_command(if_then_command, self)

    def visit_while_do_command(self, while_do_command: 'WhileDoCommand') -> None:
        pass

    def visit_do_while_command(self, do_while_command: 'DoWhileCommand') -> None:
        pass

    def visit_for_command(self, for_command: 'ForCommand') -> None:
        pass

    def visit_read_command(self, read_command: 'ReadCommand') -> None:
        # TODO change it
        self.generated_code.append(
            generate_code_for_read_command(read_command, self.declared_variables, self.declared_arrays))

    def visit_write_command(self, write_command: 'WriteCommand') -> None:
        # TODO change it
        self.generated_code.append(
            generate_code_for_write_command(write_command, self.declared_variables, self.declared_arrays))

    def visit_program(self, program: 'Program') -> str:
        # declaration are handled in __init__
        result_code: str = ""
        for code_fragment in self.generated_code:
            result_code = result_code + code_fragment
        return result_code
