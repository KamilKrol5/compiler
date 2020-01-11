from utils.AST_interpreter import *
from utils.loop_utils import compare_values_knowing_registers
from utils.math_utils import negate_number
from utils.value_utils import generate_code_for_loading_value, compute_value_register
from typing import Callable


class MathOperationsCodeGenerator:
    ONE_VAR_NAME = '@one'
    MINUS_ONE_VAR_NAME = '@minus_one'
    ZERO_VAR_NAME = '@zero'

    def __init__(self, visitor: 'ASTInterpreter'):
        self.visitor = visitor

    def _generate_code_for_addition(self, expression: ExpressionHavingTwoValues) -> str:
        if isinstance(expression.valueRight, IdentifierValue):
            if isinstance(expression.valueRight.identifier, ArrayElementByVariableIdentifier):  # dynamic
                return generate_code_for_loading_value(
                    expression.valueRight, self.visitor) + \
                       'STORE 6\n' + generate_code_for_loading_value(
                    expression.valueLeft, self.visitor) + 'ADD 6\n'
            else:
                return generate_code_for_loading_value(
                    expression.valueLeft, self.visitor) + \
                       f'ADD {compute_value_register(expression.valueRight, self.visitor)}\n'
        elif isinstance(expression.valueRight, IntNumberValue):
            return generate_code_for_loading_value(
                expression.valueRight, self.visitor) + \
                   'STORE 6\n' + generate_code_for_loading_value(
                expression.valueLeft, self.visitor) + 'ADD 6\n'
        else:
            raise ValueError('Unknown instance of Value occurred as a rightValue field in provided expression.\n')

    def _generate_code_for_subtraction(self, expression: ExpressionHavingTwoValues) -> str:
        if isinstance(expression.valueRight, IdentifierValue):
            return generate_code_for_loading_value(
                expression.valueLeft, self.visitor) + \
                   f'SUB {compute_value_register(expression.valueRight, self.visitor)}\n'
        elif isinstance(expression.valueRight, IntNumberValue):
            return generate_code_for_loading_value(expression.valueRight, self.visitor) + \
                   'STORE 6\n' + generate_code_for_loading_value(
                expression.valueLeft, self.visitor) + 'SUB 6\n'
        else:
            raise ValueError('Unknown instance of Value occurred as a rightValue field in provided expression.\n')

    def _generate_code_for_multiplication(self, expression: ExpressionHavingTwoValues) -> str:
        left_reg = 6
        right_reg = 7
        right_copy = 11
        res_reg = 8
        label_do_nothing = self.visitor.label_provider.get_label()
        label_again = self.visitor.label_provider.get_label()
        label_r_positive = self.visitor.label_provider.get_label()
        label_r_positive2 = self.visitor.label_provider.get_label()
        end = self.visitor.label_provider.get_label()
        minus_one_reg = self.visitor.declared_variables[self.MINUS_ONE_VAR_NAME]
        one_reg = self.visitor.declared_variables[self.ONE_VAR_NAME]

        result: str = f'SUB 0\n' + f'STORE {res_reg}\n' + \
                      generate_code_for_loading_value(expression.valueLeft, self.visitor) + \
                      f'STORE {left_reg}\n' + \
                      generate_code_for_loading_value(expression.valueRight, self.visitor) + \
                      f'STORE {right_reg}\n' + \
                      f'JPOS {label_r_positive}\n' + negate_number() + f'{label_r_positive}\n' \
                      f'STORE {right_copy}\n'  # if right >0 then nothing
        result = result + f'{label_again}\n' + f'LOAD {right_copy}\n' + f'SHIFT {minus_one_reg}\n' + \
            f'SHIFT {one_reg}\n' + compare_values_knowing_registers(0, right_copy) + f'JZERO {label_do_nothing}\n'  # else add left to res
        result = result + f'LOAD {res_reg}\nADD {left_reg}\nSTORE {res_reg}\n{label_do_nothing}\n'
        result = result + f'LOAD {right_copy}\nSHIFT {minus_one_reg}\nSTORE {right_copy}\n' \
            f'LOAD {left_reg}\nSHIFT {one_reg}\nSTORE {left_reg}\n'
        result = result + f'LOAD {right_copy}\nJPOS {label_again}\n' \
            f'LOAD {right_reg}\nJPOS {label_r_positive2}\nLOAD {res_reg}\n' + negate_number() + f'JUMP {end}\n' + \
                 f'{label_r_positive2}\nLOAD {res_reg}\n{end}\n'  #right > 0

        return result

    def _generate_code_for_division(self, expression: ExpressionHavingTwoValues) -> str:
        raise NotImplemented()
        # TODO

    def _generate_code_for_modulo(self, expression: ExpressionHavingTwoValues) -> str:
        raise NotImplemented()
        # TODO

    # Registers used: 0-1, 10-14
    @staticmethod
    def generate_code_for_load_ith_bit(number_reg: int, i_reg: int) -> str:
        number_shifted_i_reg = 10
        number_shifted_i_minus_one_reg = 11
        decremented_i = 12
        minus_decremented_i = 13
        negated_i = 14
        result: str = f'LOAD {i_reg}\n' + negate_number() + f'STORE {negated_i}\n' + \
            f'INC\nSTORE {minus_decremented_i}\n' + negate_number() + f'STORE {decremented_i}\n' + \
            f'LOAD {number_reg}\nSHIFT {minus_decremented_i}\nSHIFT {decremented_i}\n' + \
            f'STORE {number_shifted_i_minus_one_reg}\n' + \
            f'LOAD {number_reg}\nSHIFT {negated_i}\nSHIFT {i_reg}\nSTORE {number_shifted_i_reg}\n' + \
            f'LOAD {number_shifted_i_minus_one_reg}\nSUB {number_shifted_i_reg}\nSHIFT {minus_decremented_i}\n'

        return result

    # Registers used: 0, given1 and given2
    def generate_code_for_log(self, number_reg: int, help_reg_1: int, help_reg_2: int) -> str:
        num = help_reg_1
        value = help_reg_2
        minus_one = self.visitor.declared_variables[self.visitor.MINUS_ONE_VAR_NAME]
        label_start = self.visitor.label_provider.get_label()
        label_end = self.visitor.label_provider.get_label()
        res: str = f'LOAD {number_reg}\nSTORE {num}\nSUB 0\nSTORE {value}\n' + \
            f'{label_start}\nLOAD {num}\nSHIFT {minus_one}\nSTORE{num}\nJZERO {label_end}\n' + \
            f'LOAD {value}\nINC\nSTORE {value}\nJUMP {label_start}\n{label_end}\nLOAD {value}\n'

        return res

    expressions: Dict[str, Callable] = {
        'PLUS': _generate_code_for_addition,
        'MINUS': _generate_code_for_subtraction,
        'TIMES': _generate_code_for_multiplication,
        'DIV': _generate_code_for_division,
        'MOD': _generate_code_for_modulo
    }
