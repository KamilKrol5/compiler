from math import floor, log
from utils.utils import clean_p0

MODULO = 100
DIVISION = 200


# Negates number which is in register 0 (p0)
# Registers used: 0-1
def negate_number() -> str:
    return f'STORE 1\n' + f'SUB 0\nSUB 1\n'


# Generates constant value and stores it in destination_register
# registers used: 0-1
def generate_number(x: int, destination_register=0) -> str:
    one_register: int = 1
    result: str = clean_p0() + f'INC\nSTORE {one_register}\nDEC\n'

    for digit in bin(x)[2:-1]:
        if digit == '1':
            result = result + f'INC\nSHIFT {one_register}\n'
        elif digit == '0':
            result = result + f'SHIFT {one_register}\n'
    if bin(x)[-1] == '1':
        result = result + f'INC\n'

    if destination_register != 0:
        result = result + f'STORE {destination_register}\n'

    return result


# Result of addition in register p0
# Registers used: 2(itself) and 0-1(sub calls)
def add_constants(x: int, y: int) -> str:
    # Numbers do not have the same sign
    if x >= 0 and y <= 0:
        return generate_number(y, 2) + generate_number(x) + 'SUB 2'
    elif x <= 0 and y >= 0:
        return generate_number(x, 2) + generate_number(y) + 'SUB 2'

    # Numbers have the same sign
    result: str = generate_number(x, 2) + generate_number(y) + 'ADD 2'
    if x < 0 and y < 0:
        result = result + negate_number()
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
    result: str = generate_number(y, y_register) + generate_number(x, x_register)

    # compute the largest power of 2 smaller than y
    shifts = floor(log(y, 2))
    print(shifts)
    shifts_reg = 1

    # rest from division y / 2^shifts
    rest = y % 2 ** shifts
    print(rest)
    generate_number(rest, y_register)
    result = result + generate_number(shifts, shifts_reg)
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

    result: str = generate_number(n, n_register) + generate_number(d, d_register)
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
