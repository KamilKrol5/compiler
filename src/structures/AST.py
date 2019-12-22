from typing import List
from abc import ABC


class Value(ABC):
    pass


class Identifier(ABC):
    pass


class IntNumberValue(Value):
    def __init__(self, value: int):
        self.value = value


class IdentifierValue(Value):
    def __init__(self, identifier: Identifier):
        self.identifier = identifier


class VariableIdentifier(Identifier):
    def __init__(self, identifier_name: str):
        self.identifier_name = identifier_name


class ArrayElementByVariableIdentifier(Identifier):
    def __init__(self, array_identifier: str, index_identifier: str):
        self.array_identifier = array_identifier
        self.index_identifier = index_identifier


class ArrayElementByIntNumberIdentifier(Identifier):
    def __init__(self, array_identifier: str, index_value: IntNumberValue):
        self.array_identifier = array_identifier
        self.index_identifier = index_value


class Declaration(ABC):
    pass


class NumberDeclaration(Declaration):
    def __init__(self, identifier: str):
        self.identifier = identifier


class ArrayDeclaration(Declaration):
    def __init__(self, identifier: str, begin_index: IntNumberValue, end_index: IntNumberValue):
        self.end_index = end_index
        self.begin_index = begin_index
        self.identifier = identifier


class Declarations:
    def __init__(self, declarations: List[Declaration]):
        self.declarations = declarations

    def add_declaration(self, declaration: Declaration):
        self.declarations.append(declaration)


class Command(ABC):
    pass


class Expression(ABC):
    pass


class Condition(ABC):
    pass


class ExpressionHavingOnlyOneValue(Expression):
    def __init__(self, value: Value):
        self.value = value


class ExpressionHavingTwoValues(Expression):
    def __init__(self, value1: Value, value2: Value, operation: str):
        self.operation = operation
        self.valueLeft = value1
        self.valueRight = value2


class TwoValueCondition(Condition):
    def __init__(self, value1: Value, value2: Value, compare_operation: str):
        self.compare_operation = compare_operation
        self.valueLeft = value1
        self.valueRight = value2


class Commands:
    def __init__(self, commands: List[Command]):
        self.commands = commands

    def add_command(self, command: Command):
        self.commands.append(command)


class AssignmentCommand(Command):
    def __init__(self, identifier: Identifier, expression: Expression):
        self.expression = expression
        self.identifier = identifier


class IfThenElseCommand(Command):
    def __init__(self, condition: Condition, commands0: Commands, commands1: Commands):
        self.commands_true = commands0
        self.commands_false = commands1
        self.condition = condition


class IfThenCommand(Command):
    def __init__(self, condition: Condition, commands: Commands):
        self.commands_true = commands
        self.condition = condition


class WhileDoCommand(Command):
    def __init__(self, condition: Condition, commands: Commands):
        self.commands = commands
        self.condition = condition


class DoWhileCommand(Command):
    def __init__(self, condition: Condition, commands: Commands):
        self.commands = commands
        self.condition = condition


class ForCommand(Command):
    def __init__(self, iterator_identifier: str, start: Value, end: Value, is_down_to: bool, commands: Commands):
        self.iterator_identifier = iterator_identifier
        self.start = start
        self.end = end
        self.is_down_to = is_down_to
        self.commands = commands


class ReadCommand(Command):
    def __init__(self, identifier: Identifier):
        self.identifier = identifier


class WriteCommand(Command):
    def __init__(self, value: Value):
        self.value = value


class Program:
    def __init__(self, declarations: Declarations, commands: Commands):
        self.commands = commands
        self.declarations = declarations

# class TreeNode:
#     def __init__(self, children: List['TreeNode'], parent: 'TreeNode', child_id=0):
#         self.children: List['TreeNode'] = children
#         self.parent: TreeNode = parent
#         self.child_id: int = child_id
#
#
# class Tree:
#     def __init__(self, root: TreeNode, name='tree'):
#         self.name = name
#         self.root = root
#
#     def __str__(self):
#         return str(self.root)
#
#
# class NumberNode(TreeNode):
#     def __init__(self, children: List['TreeNode'], parent: 'TreeNode'):
#         super().__init__(children, parent)
#
#
# class BinaryOperation(TreeNode):
#     def __init__(self, children: List['TreeNode'], parent: 'TreeNode', operator: str, child_id=0):
#         super().__init__(children, parent, child_id)
#         self.operator = operator
#
#
# class WhileNode(TreeNode):
#     def __init__(self, children: List['TreeNode'], parent: 'TreeNode'):
#         super().__init__(children, parent)
#
#
# class ANumber:
#     def __init__(self, value):
#         self.value = value
