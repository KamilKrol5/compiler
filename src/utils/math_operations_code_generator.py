from structures.ast.AST import ExpressionHavingTwoValues, IntNumberValue
from utils.loop_utils import *
from utils.value_utils import generate_code_for_loading_value, compute_value_register
from typing import Callable


class MathOperationsCodeGenerator:
    def __init__(self, declared_variables: Dict[str, int],
                 declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]]):
        self.declared_arrays = declared_arrays
        self.declared_variables = declared_variables

    def _generate_code_for_addition(self, expression: ExpressionHavingTwoValues) -> str:
        if isinstance(expression.valueRight, IdentifierValue):
            return generate_code_for_loading_value(
                expression.valueLeft, self.declared_variables, self.declared_arrays) + \
                   f'ADD {compute_value_register(expression.valueRight, self.declared_variables, self.declared_arrays)}\n'
        elif isinstance(expression.valueRight, IntNumberValue):
            return generate_code_for_loading_value(
                expression.valueRight, self.declared_variables, self.declared_arrays) + \
                'STORE 6\n' + generate_code_for_loading_value(
                expression.valueLeft, self.declared_variables, self.declared_arrays) + 'ADD 6\n'
        else:
            raise ValueError('Unknown instance of Value occurred as a rightValue field in provided expression.\n')

    def _generate_code_for_subtraction(self, expression: ExpressionHavingTwoValues) -> str:
        if isinstance(expression.valueRight, IdentifierValue):
            return generate_code_for_loading_value(
                expression.valueLeft, self.declared_variables, self.declared_arrays) + \
                   f'SUB {compute_value_register(expression.valueRight, self.declared_variables, self.declared_arrays)}\n'
        elif isinstance(expression.valueRight, IntNumberValue):
            return generate_code_for_loading_value(expression.valueRight, self.declared_variables,
                                                   self.declared_arrays) + \
                   'STORE 6\n' + generate_code_for_loading_value(
                expression.valueLeft, self.declared_variables, self.declared_arrays) + 'SUB 6\n'
        else:
            raise ValueError('Unknown instance of Value occurred as a rightValue field in provided expression.\n')

    def _generate_code_for_multiplication(self, expression: ExpressionHavingTwoValues) -> str:
        left_reg = 6
        right_reg = 7
        result: str = generate_code_for_loading_value(expression.valueLeft, self.declared_variables, self.declared_arrays) +\
            f'STORE {left_reg}\n' +\
            generate_code_for_loading_value(expression.valueRight, self.declared_variables, self.declared_arrays) +\
            f'STORE {right_reg}\n'
        # TODO

        return result

    def _generate_code_for_division(self, expression: ExpressionHavingTwoValues) -> str:
        raise NotImplemented()
        # TODO

    def _generate_code_for_modulo(self, expression: ExpressionHavingTwoValues) -> str:
        raise NotImplemented()
        # TODO

    expressions: Dict[str, Callable] = {
        'PLUS': _generate_code_for_addition,
        'MINUS': _generate_code_for_subtraction,
        'TIMES': _generate_code_for_multiplication,
        'DIV': _generate_code_for_division,
        'MOD': _generate_code_for_modulo
    }
