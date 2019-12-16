from utils import *

if __name__ == '__main__':
    r = generate_number(0)
    r = r + 'PUT\n'
    r = r + generate_number(5)
    r = r + 'PUT\n'
    r = r + generate_number(32)
    r = r + 'PUT\n'
    r = r + generate_number(512)
    r = r + 'PUT\n'
    r = r + generate_number(20)
    r = r + 'PUT\n'
    r = r + add(50, 2)
    r = r + 'PUT\n'
    write_to_file('text.gb', r)
