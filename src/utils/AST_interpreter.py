from structures.ast.AST import *
from typing import Dict, Tuple

from utils.IO_utils import generate_code_for_write_command, generate_code_for_read_command
from utils.command_utils import write_code_for_if_then_command, write_code_for_if_then_else_command, \
    write_code_for_assignment_command, write_code_for_while_do_command, write_code_for_do_while_command
from utils.expression_utils import generate_code_for_expression
from utils.label_provider import LabelProvider
from utils.loop_utils import generate_condition
from utils.arrays_utils import generate_code_for_computing_index_of_array_element_by_variable, \
    compute_real_register_of_array_element
from structures.ast.identifier_register_representation import *
from utils.math_utils import generate_number
from utils.value_utils import generate_code_for_loading_value


class LocalVariableAlreadyDeclaredException(Exception):
    pass


class ASTInterpreter(Visitor):
    VARIABLES_START_REGISTER = 100
    LOCAL_VAR_SUFFIX = '@local'
    ONE_VAR_NAME = '@one'
    MINUS_ONE_VAR_NAME = '@minus_one'
    ZERO_VAR_NAME = '@zero'
    freed_variable_registers: List[int] = list()

    def __init__(self, program: Program):
        self.program: Program = program
        self.program.declarations.declarations.extend([NumberDeclaration(self.ONE_VAR_NAME),
                                                       NumberDeclaration(self.MINUS_ONE_VAR_NAME),
                                                       NumberDeclaration(self.ZERO_VAR_NAME)])

        # structures for variables
        self.declared_variables: Dict[str, int] = dict()
        self.local_variables: Dict[str, int] = dict()
        self.declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]] = dict()
        self.generated_code: List[str] = ['## Program\n']

        # label and name generators/providers
        self.label_provider: LabelProvider = LabelProvider('%label_')
        self.loop_name_provider: LabelProvider = LabelProvider('#loop')

        self._assign_registers_to_variables()
        self.generate_one_and_minus_one()

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

    def generate_one_and_minus_one(self):
        self.generated_code.append(
            generate_number(1, destination_register=self.declared_variables[self.ONE_VAR_NAME]) +
            generate_number(0, destination_register=self.declared_variables[self.ZERO_VAR_NAME]) +
            generate_number(-1, destination_register=self.declared_variables[self.MINUS_ONE_VAR_NAME]))

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

        # add local variable to list of all declared variables, name of this variable will be
        # followed by '@local' to avoid conflicts with user declared variables.
        # example: local variable 'i' will be stored as 'i@local' in <self.declared_variables> map
        self.declared_variables[self.get_local_variable_name_in_declared_variables_map(variable_name)]\
            = new_local_variable_register

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
                default_value, self.local_variables[variable_name]))

    ''' Removes previously added local variable from self.local_variables and self.declared_variables.
        local_identifier_name is variable name present in local_variables (in basic case without @local suffix).
        Example: call with 'i' as argument will remove 'i' variable from local_variables and 'i@local' from
        declared_variables.'''

    def remove_local_variable(self, local_identifier_name: str) -> None:
        self.declared_variables.pop(self.get_local_variable_name_in_declared_variables_map(local_identifier_name))
        freed_register: int = self.local_variables.pop(local_identifier_name)

        self.freed_variable_registers.append(freed_register)

    def visit_int_number_value(self, int_number_value: 'IntNumberValue') -> int:
        pass

    def visit_identifier_value(self, identifier_value: 'IdentifierValue') -> int:
        pass

    ''' Returns the real register associated with given identifier '''

    def visit_array_element_by_variable_identifier(
            self,
            array_element_by_variable_identifier: 'ArrayElementByVariableIdentifier'
    ) -> AbstractIdentifierAccess:
        return DynamicIdentifierAccess(
            generate_code_for_computing_index_of_array_element_by_variable(
                array_element_by_variable_identifier, self.declared_variables, self.declared_arrays
            ))

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

    def visit_number_declaration(self, number_declaration: 'NumberDeclaration') -> None:
        pass

    def visit_array_declaration(self, array_declaration: 'ArrayDeclaration') -> None:
        pass

    def visit_declarations(self, declarations: 'Declarations') -> None:
        pass

    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue'):
        self.generated_code.append(
            generate_code_for_expression(expression, self))

    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues'):
        self.generated_code.append(
            generate_code_for_expression(expression, self))

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
        write_code_for_while_do_command(while_do_command, self)

    def visit_do_while_command(self, do_while_command: 'DoWhileCommand') -> None:
        write_code_for_do_while_command(do_while_command, self)

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

    ''' Writes code for making JUMP to the label specified in JumpCommand.
        Method does not check if given label has any sense or if it has corresponding label in the generated code.'''

    def visit_jump_command(self, jump_command: JumpCommand) -> None:
        self.generated_code.append(
            f'JUMP {jump_command.destination_label}\n'
        )

    ''' Writes code for incrementing or decrementing a variable included in increment_decrement_command argument
        as variableIdentifier. It loads this variable, perform operation and saves result in this variable.'''

    def visit_increment_decrement_command(self, increment_decrement_command: IncrementDecrementCommand) -> None:
        code: str = generate_code_for_loading_value(
            IdentifierValue(increment_decrement_command.identifier),
            self.declared_variables, self.declared_arrays)
        if increment_decrement_command.is_decrement:
            code = code + 'DEC\n'
        else:
            code = code + 'INC\n'
        code = code + f'STORE {self.declared_variables[increment_decrement_command.identifier.identifier_name]}\n'
        self.generated_code.append(code)

    def visit_program(self, program: 'Program') -> str:
        # declaration are handled in __init__
        program.commands.accept(self)
        result_code: str = ""
        for code_fragment in self.generated_code:
            result_code = result_code + code_fragment
        return result_code
