from typing import Dict

from structures.ast.AST import *


class ConstantsFinder(Visitor, ABC):

    def __init__(self, program: 'Program', search_in_expressions=True):
        self.program = program
        self.search_in_expressions = search_in_expressions
        self.constants_found: Dict[int, int] = dict()  # value: occurrences

    def add_constant(self, number: int):
        if number in self.constants_found.values():
            self.constants_found[number] += 1
        else:
            self.constants_found[number] = 1

    @abstractmethod
    def visit_int_number_value(self, int_number_value: 'IntNumberValue'):
        self.add_constant(int_number_value.value)

    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue'):
        if self.search_in_expressions:
            expression.value.accept(self)

    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues'):
        if self.search_in_expressions:
            expression.valueLeft.accept(self)
            expression.valueRight.accept(self)
