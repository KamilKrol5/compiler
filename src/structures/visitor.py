from structures.ast.AST import *


class Visitor(ABC):

    @abstractmethod
    def visit_int_number_value(self, int_number_value: 'IntNumberValue'):
        pass

    @abstractmethod
    def visit_identifier_value(self, identifier_value: 'IdentifierValue'):
        pass

    @abstractmethod
    def visit_array_element_by_variable_identifier(
            self, array_element_by_variable_identifier: 'ArrayElementByVariableIdentifier'):
        pass

    @abstractmethod
    def visit_array_element_by_int_number_identifier(
            self, array_element_by_int_number_identifier: 'ArrayElementByIntNumberIdentifier'):
        pass

    @abstractmethod
    def visit_variable_identifier(self, variable_identifier: 'VariableIdentifier'):
        pass

    @abstractmethod
    def visit_number_declaration(self, number_declaration: 'NumberDeclaration'):
        pass

    @abstractmethod
    def visit_array_declaration(self, array_declaration: 'ArrayDeclaration'):
        pass

    @abstractmethod
    def visit_declarations(self, declarations: 'Declarations'):
        pass

    @abstractmethod
    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue'):
        pass

    @abstractmethod
    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues'):
        pass

    @abstractmethod
    def visit_two_value_condition(self, condition: 'TwoValueCondition'):
        pass

    @abstractmethod
    def visit_commands(self, commands: 'Commands'):
        pass

    @abstractmethod
    def visit_assignment_command(self, assignment_command: 'AssignmentCommand'):
        pass

    @abstractmethod
    def visit_if_then_else_command(self, if_then_else_command: 'IfThenElseCommand'):
        pass

    @abstractmethod
    def visit_if_then_command(self, if_then_command: 'IfThenCommand'):
        pass

    @abstractmethod
    def visit_while_do_command(self, while_do_command: 'WhileDoCommand'):
        pass

    @abstractmethod
    def visit_do_while_command(self, do_while_command: 'DoWhileCommand'):
        pass

    @abstractmethod
    def visit_for_command(self, for_command: 'ForCommand'):
        pass

    @abstractmethod
    def visit_read_command(self, read_command: 'ReadCommand'):
        pass

    @abstractmethod
    def visit_write_command(self, write_command: 'WriteCommand'):
        pass

    @abstractmethod
    def visit_program(self, program: 'Program'):
        pass
