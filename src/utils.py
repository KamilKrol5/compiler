# Result of addition in register p2
# Registers used: 2(itself) and 0-1(sub calls)
def add(x: int, y: int):
    result: str = generate_number(x, 2) + generate_number(y) + 'ADD 2'
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
