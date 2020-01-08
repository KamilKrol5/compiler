from utils.utils import *
from utils.math_utils import *

if __name__ == '__main__':
    # r = generate_number(0)
    # r = r + 'PUT\n'
    # r = r + generate_number(5)
    # r = r + 'PUT\n'
    # r = r + generate_number(32)
    # r = r + 'PUT\n'
    # r = r + generate_number(512)
    # r = r + 'PUT\n'
    # r = r + generate_number(20)
    # r = r + 'PUT\n'
    # r = add_constants(-50, 201)
    # r = r + 'PUT\n'
    # r = r + add_constants(-51, -21)
    # r = r + 'PUT\n'
    # r = r + add_constants(-1, 0)
    # r = r + 'PUT\n'
    # r = r + add_constants(100, -20)
    # r = r + 'PUT\n'
    # r = r + multiply_constants(5, -6)
    # r = r + 'PUT\n'
    r = divide_constants(50, 4, 'xd1', 'xd2')
    r = r + 'PUT\n'
    r = r + modulo_on_constants(50, 4, 'xd3', 'xd4')
    r = r + 'PUT\n'
    write_to_file('text.gb', r)

