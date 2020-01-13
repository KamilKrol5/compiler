from typing import Dict, List

from math import floor, log

from utils.label_provider import LabelProvider
from utils.utils import clean_p0, registers_used

MODULO = 100
DIVISION = 200

# Negates number which is in register 0 (p0)
# Registers used: 0-1
@registers_used(0, 1)
def negate_number() -> str:
    return f'STORE 1\nSUB 0\nSUB 1\n'


# Generates code for performing abs operation on the number present in register 0 (p0).
@registers_used(*negate_number.registers_used)
def generate_abs(label_provider: LabelProvider) -> str:
    label = label_provider.get_label()
    return f'JPOS {label}\n' + negate_number() + f'{label}\n'


# Generates constant value and stores it in destination_register
# registers used: 0-1
@registers_used(*negate_number.registers_used)
def generate_number(x: int, constants: Dict[str, int] = None, destination_register=0) -> str:
    if constants is None:
        constants = dict()
    constants.items()
    one_register: int = 1
    result: str = clean_p0() + f'INC\nSTORE {one_register}\nDEC\n'

    is_negative = x < 0
    x = abs(x)

    for digit in bin(x)[2:-1]:
        if digit == '1':
            result = result + f'INC\nSHIFT {one_register}\n'
        elif digit == '0':
            result = result + f'SHIFT {one_register}\n'
    if bin(x)[-1] == '1':
        result = result + f'INC\n'

    if is_negative:
        result = result + negate_number()

    if destination_register != 0:
        result = result + f'STORE {destination_register}\n'

    return result


''' Generates numbers efficiently. Generates multiple numbers from given dictionary with one loop.
    Numbers to be generated and registers where they should be stored after being generated are present dictionary.
    Key in the dictionary is number itself and value in the dictionary is register where this number should be saved.
    Returns code which generates these numbers.'''


@registers_used(2, *negate_number.registers_used)
def generate_numbers(numbers: Dict[int, int], generate_zero=False) -> str:
    one_register: int = 2
    result: str = clean_p0() + f'INC\nSTORE {one_register}\nDEC\n'
    #  abs(n): (has_pos, has_neg)
    number_signs: Dict[int, List[bool, bool]] = dict((abs(i), [False, False]) for i in numbers.keys())

    if len(numbers) == 0:
        return ''

    # if generate_zero:
    #     if 0 in numbers.keys():
    #         result = result + f'STORE {numbers[0]}\n'
    #
    # # is_number_positive = dict()
    # numbers.pop(0)
    numbers_abs = (abs(i) for i in numbers.keys())

    for n in numbers.keys():
        if n < 0:
            number_signs[abs(n)][1] = True
        else:
            number_signs[n][0] = True

    # print(number_signs)
    numbers_abs = list(set(numbers_abs))
    numbers_abs.sort()

    previous_was_negative = False
    p0: int = 0
    result = result + generate_number(numbers_abs[0])
    if number_signs[numbers_abs[0]][0]:
        result = result + f'STORE {numbers[numbers_abs[0]]}\n'
    if number_signs[numbers_abs[0]][1]:
        result = result + negate_number() + f'STORE {numbers[- numbers_abs[0]]}\n'
        previous_was_negative = True
    p0 = numbers_abs[0]

    for i in range(1, len(numbers_abs)):
        a_i = numbers_abs[i]
        a_i_m_1 = numbers_abs[i-1]
        result = result + generate_number(a_i - a_i_m_1)
        if previous_was_negative:
            result = result + f'SUB {numbers[-a_i_m_1]}\n'
        else:
            result = result + f'ADD {numbers[a_i_m_1]}\n'
        previous_was_negative = False
        #  we have our value
        if number_signs[a_i][0]:
            result = result + f'STORE {numbers[a_i]}\n'
        if number_signs[a_i][1]:
            result = result + negate_number() + f'STORE {numbers[-a_i]}\n'
            previous_was_negative = True

    return result


def generate_numbers_naive(numbers: Dict[int, int], generate_zero=False) -> str:
    result = ''
    for n, reg in numbers.items():
        result = result + generate_number(n, destination_register=reg)
    return result


# Result of addition in register p0
# Registers used: 2(itself) and 0-1(sub calls)
def add_constants(x: int, y: int) -> str:
    # Numbers do not have the same sign
    if x >= 0 and y <= 0:
        x1, y1 = abs(x), abs(y)
        return generate_number(y1, destination_register=2) + generate_number(x1) + 'SUB 2'
    elif x <= 0 and y >= 0:
        x1, y1 = abs(x), abs(y)
        return generate_number(x1, destination_register=2) + generate_number(y1) + 'SUB 2'

    # Numbers have the same sign
    result: str = generate_number(x, destination_register=2) + generate_number(y) + 'ADD 2'
    # if x < 0 and y < 0:
    #     result = result + negate_number()
    return result


# Registers used: 0-3
def multiply_constants(x: int, y: int) -> str:
    # multiplication by 0
    if x == 0 or y == 0:
        return 'SUB 0\n'

    y_register = 2
    x_register = 3
    result_is_negative = (x > 0 and y < 0) or (x < 0 and y > 0)
    x = abs(x)
    y = abs(y)
    # choose smaller number to be multiplier
    if x < y:
        y, x = x, y
        x_register, y_register = y_register, x_register
    result: str = generate_number(abs(y), destination_register=y_register) + \
        generate_number(abs(x), destination_register=x_register)

    # compute the largest power of 2 smaller than y
    shifts = floor(log(y, 2))
    print(shifts)
    shifts_reg = 1

    # rest from division y / 2^shifts
    rest = y % 2 ** shifts
    print(rest)
    generate_number(abs(rest), destination_register=y_register)
    result = result + generate_number(int(abs(shifts)), destination_register=shifts_reg)
    result = result + f'LOAD {x_register}\n' + f'SHIFT {shifts_reg}\n'
    # add the rest
    for i in range(0, rest):
        result = result + f'ADD {x_register}\n'

    # negate if number is negative
    if result_is_negative:
        result = result + negate_number()

    return result


def divide_constants(n: int, d: int, label1: str, label2: str) -> str:
    return _perform_division_with_reminder(n, d, label1, label2, DIVISION)


def modulo_on_constants(n: int, d: int, label1: str, label2: str) -> str:
    return _perform_division_with_reminder(n, d, label1, label2, MODULO)


# Performs division with reminder on positive numbers
# Registers used: 0-3
def _perform_division_with_reminder(n: int, d: int, label1: str, label2: str, desired_value: int) -> str:
    # division by 0
    if n == 0 or d == 0:
        return 'SUB 0\n'

    result_register = 1
    d_register = 2
    n_register = 3
    result_is_negative = (n > 0 and d < 0) or (n < 0 and d > 0)
    n = abs(n)
    d = abs(d)

    result: str = generate_number(n, destination_register=n_register) + \
        generate_number(d, destination_register=d_register)
    result = result + f'''SUB 0
        STORE {result_register} # res = 0
        LOAD {d_register}
        SUB {n_register} #{label1} # d - n
        JPOS #{label2} # d - n > 0 => end
        LOAD {n_register}
        SUB {d_register}
        STORE {n_register} # n = n - d
        LOAD {result_register}
        INC
        STORE {result_register}
        LOAD {d_register}
        JUMP #{label1}
        '''
    if desired_value == MODULO:
        result = result + f'LOAD {n_register} #{label2}\n'
    elif desired_value == DIVISION:
        result = result + f'LOAD {result_register} #{label2}\n'
    else:
        raise ValueError('Wrong desired_value was provided. Correct values are: MODULO, DIVISION')

    if result_is_negative:
        result = result + negate_number()

    return result
