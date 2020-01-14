from utils.AST_interpreter import *
from utils.loop_utils import compare_values_knowing_registers
from utils.math_utils import negate_number, generate_number, generate_abs
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
        if isinstance(expression.valueLeft, IntNumberValue) and isinstance(expression.valueRight, IntNumberValue):
            return generate_number(expression.valueLeft.value * expression.valueRight.value, self.visitor.constants, 0)
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

        result = [
            f'SUB 0',
            f'STORE {res_reg}',
            generate_code_for_loading_value(expression.valueLeft, self.visitor),
            f'STORE {left_reg}',
            generate_code_for_loading_value(expression.valueRight, self.visitor),
            f'STORE {right_reg}',
            f'JPOS {label_r_positive}',
            negate_number(),
            f'{label_r_positive}',
            f'STORE {right_copy}',  # if right >0 then nothing
            f'{label_again}',
            f'LOAD {right_copy}',
            f'SHIFT {minus_one_reg}',  # else add left to res ^
            f'SHIFT {one_reg}',
            compare_values_knowing_registers(0, right_copy),
            f'JZERO {label_do_nothing}',
            f'LOAD {res_reg}',
            f'ADD {left_reg}',
            f'STORE {res_reg}',
            f'{label_do_nothing}',
            f'LOAD {right_copy}',
            f'SHIFT {minus_one_reg}',
            f'STORE {right_copy}',
            f'LOAD {left_reg}',
            f'SHIFT {one_reg}',
            f'STORE {left_reg}',
            f'LOAD {right_copy}',
            f'JPOS {label_again}',
            f'LOAD {right_reg}',
            f'JPOS {label_r_positive2}',
            f'LOAD {res_reg}',
            negate_number(),
            f'JUMP {end}',
            f'{label_r_positive2}',
            f'LOAD {res_reg}',
            f'{end}'  # right > 0
        ]

        return '\n'.join(result) + '\n'

    # Registers used: 0-?, 10-23
    def _generate_code_for_division(self, expression: ExpressionHavingTwoValues) -> str:
        return self._generate_code_for_division_or_modulo(expression, is_modulo=False)

    # Registers used: 0-?, 10-23
    def _generate_code_for_modulo(self, expression: ExpressionHavingTwoValues) -> str:
        return self._generate_code_for_division_or_modulo(expression, is_modulo=True)

    # Registers used: 0-?, 10-23
    def _generate_code_for_division_or_modulo(self, expression: ExpressionHavingTwoValues, is_modulo: bool) -> str:
        if isinstance(expression.valueLeft, IntNumberValue) and isinstance(expression.valueRight, IntNumberValue):
            if expression.valueRight.value != 0:
                if is_modulo:
                    return generate_number(
                        expression.valueLeft.value % expression.valueRight.value, self.visitor.constants, 0)
                else:
                    return generate_number(
                        expression.valueLeft.value // expression.valueRight.value, self.visitor.constants, 0)
            else:
                return generate_number(0, self.visitor.constants)

        divisor = 22
        divisor_abs = 15
        number = 23
        number_abs = 16
        reminder = 17
        quotient = 18
        counter = 19
        log = 20
        register_to_return = reminder if is_modulo else quotient
        minus_one = self.visitor.declared_variables[self.MINUS_ONE_VAR_NAME]
        one = self.visitor.declared_variables[self.ONE_VAR_NAME]

        label_zero = self.visitor.label_provider.get_label()
        label_start = self.visitor.label_provider.get_label()
        label_end = self.visitor.label_provider.get_label()
        label_if = self.visitor.label_provider.get_label()
        label_end2 = self.visitor.label_provider.get_label()
        label_divisor_neg = self.visitor.label_provider.get_label()
        label_number_neg = self.visitor.label_provider.get_label()
        label_both_neg = self.visitor.label_provider.get_label()
        label_finish = self.visitor.label_provider.get_label()
        label_finish1 = self.visitor.label_provider.get_label()
        label_finish2 = self.visitor.label_provider.get_label()

        code_1: List[str] = [
            f'## BEGIN div',
            generate_code_for_loading_value(expression.valueRight, self.visitor),
            f'STORE {divisor}',  # save right value
            f'JZERO {label_zero}',  # if right value is 0, we can end returning 0
            f'SUB 0',
            f'STORE {reminder}',
            f'STORE {quotient}',  # quotient = 0, reminder = 0
            generate_code_for_loading_value(expression.valueLeft, self.visitor),
            f'STORE{number}',  # save left value
            generate_abs(self.visitor.label_provider),
            f'STORE{number_abs}',
            f'LOAD{divisor}',
            generate_abs(self.visitor.label_provider),
            f'STORE{divisor_abs}',  # division uses only positive numbers, so abs was called
            # f'LOAD {number_abs}',
            # f'SHIFT {one}',
            # f'STORE {number_copy}',
            self.generate_code_for_log(number_abs, counter, 21),  # we iterate log(n) + 1 times
            f'INC',
            f'STORE {counter}',  # counter = log(n) + 1
            f'INC',
            f'STORE {log}',
        ]
        code_2: List[str] = [
            f'{label_start}',  # beginning of a loop
            f'LOAD {log}',
            f'DEC',
            f'STORE {log}',
            f'JZERO {label_end}',
            f'LOAD {reminder}',
            f'SHIFT {one}',
            f'STORE {reminder}',  # reminder = reminder << 1
            self.generate_code_for_load_ith_bit(number_abs, counter),
            f'ADD {reminder}',
            f'STORE {reminder}',  # reminder = reminder + counter'th bit of number; R(0) = N(counter)
            compare_values_knowing_registers(reminder, divisor_abs),
            f'JNEG {label_if}',  # if reminder >= divisor_abs, if not jump to label_if
            f'STORE {reminder}',  # reminder = reminder - divisor_abs
            f'LOAD {quotient}',
            f'INC',
            f'STORE {quotient}',  # quotient++
            f'{label_if}',
            f'LOAD {quotient}',
            f'SHIFT {one}',
            f'STORE {quotient}',  # quotient << 1
            f'LOAD {counter}',
            f'DEC',
            f'STORE {counter}',  # counter--
            f'JUMP {label_start}',
        ]

        code_3 = [
            f'{label_zero}',
            f'SUB 0',  # load zero
            f'JUMP {label_end2}',  # work is done
            f'{label_end}',  # end of loop, almost ready to return values
            f'LOAD {quotient}',
            f'SHIFT {minus_one}',
            f'STORE {quotient}',  # quotient = quotient >> 1,
            # because in the last iteration it was shifted left unnecessarily
        ]
        #  return
        code_4 = [
            f'LOAD {divisor}',
            f'JNEG {label_divisor_neg}',  # here divisor is positive so reminder will be positive
            f'LOAD {number}',
            f'JNEG {label_number_neg}',
            f'JUMP {label_finish}',
            f'{label_divisor_neg}',
            f'LOAD {number}',
            f'JNEG {label_both_neg}',
            f'LOAD {quotient}',
            f'INC',
            negate_number(),
            f'STORE {quotient}',
            f'LOAD {reminder}',
            f'SUB {divisor_abs}',
            f'STORE {reminder}',
            f'JUMP {label_finish1}',
            f'{label_number_neg}',  # here divisor is positive and number is negative
            f'LOAD {quotient}',
            f'INC',
            negate_number(),
            f'STORE {quotient}',
            f'LOAD {divisor_abs}',
            f'SUB {reminder}',
            f'STORE {reminder}',
            f'JUMP {label_finish2}',
            f'{label_both_neg}',
            f'LOAD {reminder}',
            negate_number(),
            f'STORE {reminder}',
            f'{label_finish}',
            f'{label_finish1}',
            f'{label_finish2}',
            f'LOAD {register_to_return}',
            f'{label_end2}',
        ]
        return '\n'.join(code_1) + '\n' + \
               '\n'.join(code_2) + '\n' + \
               '\n'.join(code_3) + '\n' + \
               '\n'.join(code_4) + '\n## END div\n'

    # Registers used: 0-1, 10-14
    @staticmethod
    def generate_code_for_load_ith_bit(number_reg: int, i_reg: int) -> str:
        number_shifted_i_reg = 10
        number_shifted_i_minus_one_reg = 11
        decremented_i = 12
        minus_decremented_i = 13
        negated_i = 14
        result: List[str] = [
            f'LOAD {i_reg}',
            negate_number(),
            f'STORE {negated_i}',
            f'INC',
            f'STORE {minus_decremented_i}',
            negate_number(),
            f'STORE {decremented_i}',
            f'LOAD {number_reg}',
            f'SHIFT {minus_decremented_i}',
            f'SHIFT {decremented_i}',
            f'STORE {number_shifted_i_minus_one_reg}',
            f'LOAD {number_reg}',
            f'SHIFT {negated_i}',
            f'SHIFT {i_reg}',
            f'STORE {number_shifted_i_reg}',
            f'LOAD {number_shifted_i_minus_one_reg}',
            f'SUB {number_shifted_i_reg}',
            f'SHIFT {minus_decremented_i}',
        ]

        return '\n'.join(result) + '\n'

    # Registers used: 0, given1 and given2
    def generate_code_for_log(self, number_reg: int, help_reg_1: int, help_reg_2: int) -> str:
        num = help_reg_1
        value = help_reg_2
        minus_one = self.visitor.declared_variables[self.visitor.MINUS_ONE_VAR_NAME]
        label_start = self.visitor.label_provider.get_label()
        label_end = self.visitor.label_provider.get_label()
        res: List[str] = [
            f'LOAD {number_reg}',
            f'STORE {num}',
            f'SUB 0',
            f'STORE {value}',
            f'{label_start}',
            f'LOAD {num}',
            f'SHIFT {minus_one}',
            f'STORE {num}',
            f'JZERO {label_end}',
            f'LOAD {value}',
            f'INC',
            f'STORE {value}',
            f'JUMP {label_start}',
            f'{label_end}',
            f'LOAD {value}',
        ]

        return '\n'.join(res) + '\n'

    expressions: Dict[str, Callable] = {
        'PLUS': _generate_code_for_addition,
        'MINUS': _generate_code_for_subtraction,
        'TIMES': _generate_code_for_multiplication,
        'DIV': _generate_code_for_division,
        'MOD': _generate_code_for_modulo
    }
