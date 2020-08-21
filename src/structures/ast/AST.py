from typing import List, Tuple
from abc import ABC, abstractmethod
from structures.visitor import Visitor

INDENT: str = '   '


class ASTElement:
    start_position: Tuple[int, int] = (0, 0)

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class PrintableWithIndent:
    @abstractmethod
    def to_str_with_indent(self, indent=0) -> str:
        pass


class Value(ABC, ASTElement, PrintableWithIndent):
    """ Returns if value can be known statically."""
    @abstractmethod
    def is_static(self) -> bool:
        pass


class Identifier(ABC, ASTElement, PrintableWithIndent):
    pass


class IntNumberValue(Value):
    def accept(self, visitor: Visitor):
        return visitor.visit_int_number_value(self)

    def is_static(self) -> bool:
        return True

    def __init__(self, value: int, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.value = value

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<IntNumberValue[ value = {self.value} ]>'


class IdentifierValue(Value):
    def accept(self, visitor: Visitor):
        return visitor.visit_identifier_value(self)

    def __init__(self, identifier: Identifier, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.identifier = identifier

    def is_static(self) -> bool:
        return False

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<IdentifierValue[ ' \
            f'identifier = \n{self.identifier.to_str_with_indent(indent + 1)}\n' \
            + indent * INDENT + ']>'


class VariableIdentifier(Identifier):
    def accept(self, visitor: Visitor):
        return visitor.visit_variable_identifier(self)

    def __init__(self, identifier_name: str, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.identifier_name = identifier_name

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<VariableIdentifier[ identifier_name = {self.identifier_name} ]>'

    def __str__(self):
        return self.identifier_name


class ArrayElementByVariableIdentifier(Identifier):
    def accept(self, visitor: Visitor):
        return visitor.visit_array_element_by_variable_identifier(self)

    def __init__(self, array_identifier: str, index_identifier: str, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.array_identifier = array_identifier
        self.index_identifier = index_identifier

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ArrayElementByVariableIdentifier[ array_identifier = {self.array_identifier}, ' \
            f'index_identifier = {self.index_identifier} ]>'

    def __str__(self):
        return self.array_identifier + f'({self.index_identifier})'


class ArrayElementByIntNumberIdentifier(Identifier):
    def accept(self, visitor: Visitor):
        return visitor.visit_array_element_by_int_number_identifier(self)

    def __init__(self, array_identifier: str, index_value: IntNumberValue, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.array_identifier = array_identifier
        self.index_value = index_value

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ArrayElementByIntNumberIdentifier[ array_identifier = {self.array_identifier}, ' \
            f'index_value = \n{self.index_value.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + ']>'

    def __str__(self):
        return f'{self.array_identifier}({self.index_value.value})'


class Declaration(ABC, ASTElement, PrintableWithIndent):
    identifier = None
    pass


class NumberDeclaration(Declaration):
    def accept(self, visitor: Visitor):
        return visitor.visit_number_declaration(self)

    def __init__(self, identifier: str, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.identifier = identifier

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<NumberDeclaration[ id = {self.identifier} ]>'


class ArrayDeclaration(Declaration):
    def accept(self, visitor: Visitor):
        return visitor.visit_array_declaration(self)

    def __init__(self, identifier: str, begin_index: IntNumberValue, end_index: IntNumberValue, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.end_index = end_index
        self.begin_index = begin_index
        self.identifier = identifier

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ArrayDeclaration[ id = {self.identifier}, begin_index = ' + \
               f'\n{self.begin_index.to_str_with_indent(indent + 1)},\n' + \
               indent * INDENT + f'end_index = \n' + \
               f'{self.end_index.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + f']>'


class Declarations(ASTElement, PrintableWithIndent):
    def accept(self, visitor: Visitor):
        return visitor.visit_declarations(self)

    def __init__(self, declarations: List[Declaration], start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.declarations = declarations

    def add_declaration(self, declaration: Declaration) -> None:
        self.declarations.append(declaration)

    def to_str_with_indent(self, indent=0) -> str:
        return str(('\n' + (indent * INDENT)).join(map(lambda x: x.to_str_with_indent(indent + 1), self.declarations)))


class Command(ABC, ASTElement, PrintableWithIndent):
    pass


class Expression(ABC, ASTElement, PrintableWithIndent):
    @abstractmethod
    def number_of_values(self) -> int:
        pass


class Condition(ABC, ASTElement, PrintableWithIndent):
    pass


class ExpressionHavingOneValue(Expression):
    def accept(self, visitor: Visitor):
        return visitor.visit_expression_having_one_value(self)

    def __init__(self, value: Value, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.value = value

    def number_of_values(self) -> int:
        return 1

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ExpressionHavingOnlyOneValue[ value = ' \
            f'\n{self.value.to_str_with_indent(indent + 1)}\n' + indent * INDENT + f']>'


class ExpressionHavingTwoValues(Expression):
    def accept(self, visitor: Visitor):
        return visitor.visit_expression_having_two_values(self)

    def __init__(self, value1: Value, value2: Value, operation: str, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.operation = operation
        self.valueLeft = value1
        self.valueRight = value2

    def number_of_values(self) -> int:
        return 2

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ExpressionHavingTwoValues[' \
               f' value_left = \n{self.valueLeft.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + f'value_right = \n{self.valueRight.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + f'operation = {self.operation}\n' + indent * INDENT + ']>'


class TwoValueCondition(Condition):

    def accept(self, visitor: Visitor):
        return visitor.visit_two_value_condition(self)

    def __init__(self, value1: Value, value2: Value, compare_operation: str, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.compare_operation = compare_operation
        self.valueLeft = value1
        self.valueRight = value2

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<TwoValueCondition[' \
               f'value_left = \n{self.valueLeft.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + f'value_right = \n{self.valueRight.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + f'operation = {self.compare_operation}\n' + indent * INDENT + ']>'


class Commands(ASTElement, PrintableWithIndent):
    def accept(self, visitor: Visitor):
        return visitor.visit_commands(self)

    def __init__(self, commands: List[Command], start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.commands = commands

    def add_command(self, command: Command) -> None:
        self.commands.append(command)

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + str(('\n' + (indent * INDENT))
                                     .join(map(lambda x: x.to_str_with_indent(indent + 1), self.commands)))


class AssignmentCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_assignment_command(self)

    def __init__(self, identifier: Identifier, expression: Expression, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.expression = expression
        self.identifier = identifier

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<AssignmentCommand[ ' \
               f'identifier = \n{self.identifier.to_str_with_indent(indent + 1)} \n' + \
               indent * INDENT + f'expression = \n{self.expression.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + f']>'


class IfThenElseCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_if_then_else_command(self)

    def __init__(
            self,
            condition: Condition,
            commands_true: Commands,
            commands_false: Commands,
            start_position=(0, 0)
    ):
        self.start_position: Tuple[int, int] = start_position
        self.commands_true = commands_true
        self.commands_false = commands_false
        self.condition = condition

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<IfThenElseCommand[ condition = \n' \
            f'{self.condition.to_str_with_indent(indent+1)},\n' +\
            indent * INDENT + f'commands_true =\n' \
            f'{self.commands_true.to_str_with_indent(indent+1)}\n' +\
            indent * INDENT + f'commands_false =\n' \
            f'{self.commands_false.to_str_with_indent(indent+1)}\n' +\
            indent * INDENT + f']> '


class IfThenCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_if_then_command(self)

    def __init__(self, condition: Condition, commands: Commands, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.commands_true = commands
        self.condition = condition

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<IfThenCommand[ condition = \n' \
            f'{self.condition.to_str_with_indent(indent + 1)},\n' + \
            indent * INDENT + f'commands_true =\n' \
            f'{self.commands_true.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + f']> '


class WhileDoCommand(Command):

    def accept(self, visitor: Visitor):
        return visitor.visit_while_do_command(self)

    def __init__(self, condition: Condition, commands: Commands, is_user_command=True, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.commands = commands
        self.condition = condition
        self.is_user_command = is_user_command

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<WhileDoCommand[ condition =\n' \
            f'{self.condition.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + f'commands = \n' \
            f'{self.commands.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + ']>'


class DoWhileCommand(Command):

    def accept(self, visitor: Visitor):
        return visitor.visit_do_while_command(self)

    def __init__(self, condition: Condition, commands: Commands, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.commands = commands
        self.condition = condition

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<DoWhileCommand[ condition =\n' \
            f'{self.condition.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + f'commands = \n' \
            f'{self.commands.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + ']>'


class ForCommand(Command):

    def accept(self, visitor: Visitor):
        return visitor.visit_for_command(self)

    def __init__(
            self,
            iterator_identifier: str,
            start: Value,
            end: Value,
            is_down_to: bool,
            commands: Commands,
            start_position=(0, 0)
    ):
        self.start_position: Tuple[int, int] = start_position
        self.iterator_identifier = iterator_identifier
        self.start = start
        self.end = end
        self.is_down_to = is_down_to
        self.commands = commands

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ForCommand[ iterator_identifier = {self.iterator_identifier}, ' \
            f'is_down_to = {self.is_down_to}, start = \n' + \
            f'{self.start.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + f'end =\n' \
            f'{self.end.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + f'commands = \n' \
            f'{self.commands.to_str_with_indent(indent + 1)}\n' + \
            indent * INDENT + ']>'


class ReadCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_read_command(self)

    def __init__(self, identifier: Identifier, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.identifier = identifier

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<ReadCommand[ id = \n{self.identifier.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + ']>'


class WriteCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_write_command(self)

    def __init__(self, value: Value, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.value = value

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<WriteCommand[ value = \n{self.value.to_str_with_indent(indent + 1)}\n' + \
               indent * INDENT + ']>'


class JumpCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_jump_command(self)

    def __init__(self, destination_label: str, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.destination_label = destination_label

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<*JumpCommand[ destination_label = {self.destination_label}\n' + \
               indent * INDENT + ']>'


class IncrementDecrementCommand(Command):
    def accept(self, visitor: Visitor):
        return visitor.visit_increment_decrement_command(self)

    def __init__(
            self,
            identifier: VariableIdentifier,
            is_decrement=False,
            start_position=(0, 0)
    ):
        self.start_position: Tuple[int, int] = start_position
        self.identifier = identifier
        self.is_decrement = is_decrement

    def to_str_with_indent(self, indent=0) -> str:
        return indent * INDENT + f'<*IncrementDecrementCommand[ is_decrement = {self.is_decrement}, identifier = ' \
               f'{self.identifier.to_str_with_indent(indent + 1)} ]' + \
               indent * INDENT + ']>'


class Program(ASTElement):
    def accept(self, visitor: Visitor) -> str:
        return visitor.visit_program(self)

    def __init__(self, declarations: Declarations, commands: Commands, start_position=(0, 0)):
        self.start_position: Tuple[int, int] = start_position
        self.commands = commands
        self.declarations = declarations

    def __str__(self):
        return "Declarations:\n" + str(self.declarations.to_str_with_indent(0)) + "\nCommands:\n" + str(
            self.commands.to_str_with_indent(0))
