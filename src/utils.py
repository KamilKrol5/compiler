from math import log, floor


# Negates number which is in register 0 (p0)
# Registers used: 0-1
def negate_number() -> str:
    return f'STORE 1\n' + f'SUB 0\nSUB 1'


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


# no registers used
def write_to_file(filename: str, text: str, append_halt=True):
    if append_halt:
        text = text + 'HALT'
    with open(filename, "w", newline='\n') as file:
        file.write(text + '\n')


# no registers used
def clean_p0() -> str:
    return 'SUB 0\n'


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
