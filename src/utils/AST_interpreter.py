from structures.ast.AST import *
from typing import Dict, Tuple, Iterable

from structures.constants_finder import ConstantsFinder
from utils.IO_utils import generate_code_for_write_command, generate_code_for_read_command
from utils.command_utils import write_code_for_if_then_command, write_code_for_if_then_else_command, \
    write_code_for_assignment_command, write_code_for_while_do_command, write_code_for_do_while_command, \
    write_code_for_for_loop_command
from utils.expression_utils import generate_code_for_expression
from utils.label_provider import LabelProvider
from utils.loop_utils import generate_condition
from utils.arrays_utils import generate_code_for_computing_index_of_array_element_by_variable, \
    compute_real_register_of_array_element
from structures.ast.identifier_register_representation import *
from utils.math_utils import generate_number, generate_numbers, generate_numbers_naive
from utils.value_utils import generate_code_for_loading_value


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


class DefaultConstant:
    def __init__(self, name: str, value: int):
        self.name: str = name
        self.value: int = value


class ASTInterpreter(Visitor):
    VARIABLES_START_REGISTER = 100
    LOCAL_VAR_SUFFIX = '@local'
    ONE_VAR_NAME = '@one'
    MINUS_ONE_VAR_NAME = '@minus_one'
    ZERO_VAR_NAME = '@zero'
    CONSTANT_SUFFIX = '@const'
    default_constants = [
        DefaultConstant(ONE_VAR_NAME, 1),
        DefaultConstant(MINUS_ONE_VAR_NAME, -1),
        DefaultConstant(ZERO_VAR_NAME, 0),
    ]
    freed_variable_registers: List[int] = list()

    def __init__(self, program: Program):
        self.program: Program = program
        # constants preparation
        self.constants_finder = ConstantsFinder(self.program, search_in_expressions=False)
        constants = self.constants_finder.find_constants().keys()
        self.program.declarations.declarations.extend([NumberDeclaration(self.ONE_VAR_NAME),
                                                       NumberDeclaration(self.MINUS_ONE_VAR_NAME),
                                                       NumberDeclaration(self.ZERO_VAR_NAME)])
        self.program.declarations.declarations.extend(NumberDeclaration(str(c)+self.CONSTANT_SUFFIX) for c in constants)

        # structures for variables
        self.declared_variables: Dict[str, int] = dict()
        self.local_variables: Dict[str, int] = dict()
        self.declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]] = dict()
        self.shadowed_variables: Dict[str, List[int]] = dict()
        self.generated_code: List[str] = ['## Program\n']

        # label and name generators/providers
        self.label_provider: LabelProvider = LabelProvider('%label_')
        self.loop_name_provider: LabelProvider = LabelProvider('#loop')

        self._assign_registers_to_variables()

        # generating constants
        self.generate_default_constants()
        self.generate_constants(constants)
        self.constants: Dict[int, int] = dict(
            (const,
             self.declared_variables[str(const)+self.CONSTANT_SUFFIX])
            for const in self.constants_finder.constants_found.keys())
        # pprint(self.constants)
        # pprint(self.declared_variables)
        # pprint(self.declared_arrays)

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
        print(f'Variables start register: {self.VARIABLES_START_REGISTER}')

    ''' Generates default constants and stores them in specified registers.
        Names of the constants need to be present in declared_variables before call of this method.'''

    def generate_default_constants(self):
        for const in self.default_constants:
            self.generated_code.append(
                generate_number(const.value, {}, destination_register=self.declared_variables[const.name]))

    def generate_constants(self, constants: Iterable[int]):
        numbers: Dict[int, int] = \
            dict((const, self.declared_variables[str(const)+self.CONSTANT_SUFFIX]) for const in constants)
        self.generated_code.append(generate_numbers(numbers))

    ''' Returns local variable key in the declared_variables map.
        Example: call with argument 'i' will return 'i@local'.'''

    def get_local_variable_name_in_declared_variables_map(self, variable_name: str) -> str:
        return variable_name + self.LOCAL_VAR_SUFFIX

    ''' Add local variable to the interpreter. If there was the same variable already declared 
        an LocalVariableAlreadyDeclaredException is raised. 
        More details below - in method comments.'''

    def add_local_variable(self, variable_name: str, default_value=None) -> None:
        # An assumption: there cannot be two nested local variables named the same.
        if variable_name in self.local_variables or \
            self.get_local_variable_name_in_declared_variables_map(variable_name) \
                in self.declared_variables:
            raise LocalVariableAlreadyDeclaredException(f'Local variable with "{variable_name}" was '
                                                        f'already defined.')

        # self.program.declarations.declarations.append(number_declaration) not needed
        if len(self.freed_variable_registers) != 0:
            new_local_variable_register = self.freed_variable_registers.pop()
        else:
            new_local_variable_register = self.VARIABLES_START_REGISTER + 1
            self.VARIABLES_START_REGISTER = self.VARIABLES_START_REGISTER + 1  # incrementation right after assignment

        # if there is already variable with the same name defined, it will be shadowed.
        # To the shadowed_variables dictionary will be added a stack (list) for this variable name.
        # Previous register stored in declared_arrays will be pushed to the stack and when removing a local variable
        # it can be assigned again to the variable in declared_arrays dictionary.
        if variable_name in self.declared_variables.keys():
            if variable_name not in self.shadowed_variables.keys():
                self.shadowed_variables[variable_name] = [self.declared_variables[variable_name]]
            else:
                self.shadowed_variables[variable_name].append(self.declared_variables[variable_name])

        # add local variable to list of all declared variables, name of this variable will be
        # followed by '@local' to avoid conflicts with user declared variables.
        # example: local variable 'i' will be stored as 'i@local' in <self.declared_variables> map
        self.declared_variables[variable_name] = new_local_variable_register

        # a new variable needs also to be added to <self.local_variables> map,
        # it will allow shadowing mechanism in for loop.
        # An assignment command can check if left-side-assignment variable
        # is present in local variables, if it is, then it cannot be modified and the access to this variable should
        # be performed with @local postfix.
        # Example: Let's assume we have user declared variable 'k', and now we declare local variable names also 'k',
        # (ex. for loop with iterator k). After adding local(!) variable named'k':
        #       - 'k' and 'k@local' is present in <self.declared_variables>
        #       - 'k' is present in <self.local_variables>
        # Now in the for loop: If someone wants to assign value to 'k' variable, the assignment command will know
        # that it is local variable (or later changed to loop/iterator variable) and it cannot be modified, so
        # error can be detected. If someone wants to read value of variable 'k' (still in a for loop) reading procedure
        # can check if it is local variable now. if it is the value should be read from 'k@local' variable. There is
        # no need to check both maps with variables. In the end of scope of local variable it has to be removed!
        self.local_variables[variable_name] = new_local_variable_register
        # If default value is provided the code for assigning new variable with default value will be generated
        if default_value is not None:
            # assume tht default_value is type int
            self.generated_code.append(generate_number(
                default_value, constants=self.constants, destination_register=self.local_variables[variable_name]))

    ''' Removes previously added local variable from self.local_variables and self.declared_variables.
        local_identifier_name is variable name present in local_variables (in basic case without @local suffix).
        Example: call with 'i' as argument will remove 'i' variable from local_variables and 'i@local' from
        declared_variables.'''

    def remove_local_variable(self, local_identifier_name: str) -> None:
        if local_identifier_name not in self.declared_variables:
            raise AnAttemptToRemoveNonExistingLocalVariable(
                f"An attempt to remove non existing local variable: {local_identifier_name}.")

        if local_identifier_name in self.shadowed_variables:
            if len(self.shadowed_variables[local_identifier_name]) != 0:
                prev_reg: int = self.shadowed_variables[local_identifier_name].pop()
                self.declared_variables[local_identifier_name] = prev_reg
                if len(self.shadowed_variables[local_identifier_name]) == 0:
                    self.shadowed_variables.pop(local_identifier_name)
            else:
                self.declared_variables.pop(local_identifier_name)
        else:
            self.declared_variables.pop(local_identifier_name)

        freed_register: int = self.local_variables.pop(local_identifier_name)
        self.freed_variable_registers.append(freed_register)

    def is_identifier_local_variable(self, identifier: Identifier) -> bool:
        return isinstance(identifier, VariableIdentifier) and identifier.identifier_name in self.local_variables

    def visit_identifier_value(self, identifier_value: 'IdentifierValue') -> int:
        pass

    ''' Returns the real register associated with given identifier '''

    def visit_array_element_by_variable_identifier(
            self,
            array_element_by_variable_identifier: 'ArrayElementByVariableIdentifier'
    ) -> AbstractIdentifierAccess:
        return DynamicIdentifierAccess(
            generate_code_for_computing_index_of_array_element_by_variable(
                array_element_by_variable_identifier, self))

    ''' Returns the real register associated with given identifier '''

    def visit_array_element_by_int_number_identifier(
            self,
            array_element_by_int_number_identifier: 'ArrayElementByIntNumberIdentifier'
    ) -> AbstractIdentifierAccess:
        return StaticIdentifierAccess(
            compute_real_register_of_array_element(
                self.declared_arrays, array_element_by_int_number_identifier)
        )

    ''' Returns the real register associated with given identifier '''

    def visit_variable_identifier(
            self, variable_identifier: 'VariableIdentifier') -> AbstractIdentifierAccess:
        return StaticIdentifierAccess(
            self.declared_variables[variable_identifier.identifier_name]
        )

    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue'):
        self.generated_code.append(
            generate_code_for_expression(expression, self))

    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues'):
        self.generated_code.append(
            generate_code_for_expression(expression, self))

    def visit_two_value_condition(self, condition: 'TwoValueCondition'):
        # TODO change it
        self.generated_code.append(
            generate_condition(condition, self))

    def visit_assignment_command(self, assignment_command: 'AssignmentCommand') -> None:
        write_code_for_assignment_command(assignment_command, self)

    def visit_if_then_else_command(self, if_then_else_command: 'IfThenElseCommand') -> None:
        write_code_for_if_then_else_command(if_then_else_command, self)

    def visit_if_then_command(self, if_then_command: 'IfThenCommand') -> None:
        write_code_for_if_then_command(if_then_command, self)

    def visit_while_do_command(self, while_do_command: 'WhileDoCommand') -> None:
        write_code_for_while_do_command(while_do_command, self)

    def visit_do_while_command(self, do_while_command: 'DoWhileCommand') -> None:
        write_code_for_do_while_command(do_while_command, self)

    def visit_for_command(self, for_command: 'ForCommand') -> None:
        write_code_for_for_loop_command(for_command, self)

    def visit_read_command(self, read_command: 'ReadCommand') -> None:
        self.generated_code.append(
            generate_code_for_read_command(read_command, self))

    def visit_write_command(self, write_command: 'WriteCommand') -> None:
        self.generated_code.append(
            generate_code_for_write_command(write_command, self))

    ''' Writes code for making JUMP to the label specified in JumpCommand.
        Method does not check if given label has any sense or if it has corresponding label in the generated code.'''

    def visit_jump_command(self, jump_command: JumpCommand) -> None:
        self.generated_code.append(
            f'JUMP {jump_command.destination_label}\n')

    ''' Writes code for incrementing or decrementing a variable included in increment_decrement_command argument
        as variableIdentifier. It loads this variable, perform operation and saves result in this variable.'''

    def visit_increment_decrement_command(self, increment_decrement_command: IncrementDecrementCommand) -> None:
        code: str = generate_code_for_loading_value(
            IdentifierValue(increment_decrement_command.identifier), self)
        if increment_decrement_command.is_decrement:
            code = code + 'DEC\n'
        else:
            code = code + 'INC\n'

        if increment_decrement_command.identifier.identifier_name in self.local_variables:
            code = code + f'STORE {self.local_variables[increment_decrement_command.identifier.identifier_name]}\n'
        else:
            code = code + f'STORE {self.declared_variables[increment_decrement_command.identifier.identifier_name]}\n'
        self.generated_code.append(code)

    def visit_program(self, program: 'Program') -> str:
        # declaration are handled in __init__
        program.commands.accept(self)
        result_code: str = ""
        for code_fragment in self.generated_code:
            result_code = result_code + code_fragment
        return result_code
