from structures.ast.AST import *


class Visitor(ABC):

    @abstractmethod
    def visit_int_number_value(self, int_number_value: 'IntNumberValue') -> str:
        pass

    @abstractmethod
    def visit_identifier_value(self, identifier_value: 'IdentifierValue') -> str:
        pass

    @abstractmethod
    def visit_array_element_by_variable_identifier(
            self, array_element_by_variable_identifier: 'ArrayElementByVariableIdentifier') -> str:
        pass

    @abstractmethod
    def visit_array_element_by_int_number_identifier(
            self, array_element_by_int_number_identifier: 'ArrayElementByIntNumberIdentifier') -> str:
        pass

    @abstractmethod
    def visit_variable_identifier(self, variable_identifier: 'VariableIdentifier') -> str:
        pass

    @abstractmethod
    def visit_number_declaration(self, number_declaration: 'NumberDeclaration') -> str:
        pass

    @abstractmethod
    def visit_array_declaration(self, array_declaration: 'ArrayDeclaration') -> str:
        pass

    @abstractmethod
    def visit_declarations(self, declarations: 'Declarations') -> str:
        pass

    @abstractmethod
    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue') -> str:
        pass

    @abstractmethod
    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues') -> str:
        pass

    @abstractmethod
    def visit_two_value_condition(self, condition: 'TwoValueCondition') -> str:
        pass

    @abstractmethod
    def visit_commands(self, commands: 'Commands') -> str:
        pass

    @abstractmethod
    def visit_assignment_command(self, assignment_command: 'AssignmentCommand') -> str:
        pass

    @abstractmethod
    def visit_if_then_else_command(self, if_then_else_command: 'IfThenElseCommand') -> str:
        pass

    @abstractmethod
    def visit_if_then_command(self, if_then_command: 'IfThenCommand') -> str:
        pass

    @abstractmethod
    def visit_while_do_command(self, while_do_command: 'WhileDoCommand') -> str:
        pass

    @abstractmethod
    def visit_do_while_command(self, do_while_command: 'DoWhileCommand') -> str:
        pass

    @abstractmethod
    def visit_for_command(self, for_command: 'ForCommand') -> str:
        pass

    @abstractmethod
    def visit_read_command(self, read_command: 'ReadCommand') -> str:
        pass

    @abstractmethod
    def visit_write_command(self, write_command: 'WriteCommand') -> str:
        pass

    @abstractmethod
    def visit_program(self, program: 'Program') -> str:
        pass
