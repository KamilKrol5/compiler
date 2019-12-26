from utils.IO_utils import *
from utils.utils import write_to_file

decl_vars = {"c": 32, "d": 64}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}


def test_read():
    code = generate_code_for_read_command(ReadCommand(VariableIdentifier('c')), decl_vars, decl_arrays)
    code = code + 'LOAD 32\nPUT\n'
    write_to_file('io_test.txt', code)


# Expected: 45, 555, 2, -666, -2000
def test_write():
    code: str = generate_number(555, 32) + generate_number(2, 64) + generate_number(-2000, 125) + generate_number(-666, 142)
    code = code + generate_code_for_write_command(WriteCommand(IntNumberValue(45)), decl_vars, decl_arrays)
    code = code + generate_code_for_write_command(WriteCommand(IdentifierValue(VariableIdentifier('c'))), decl_vars, decl_arrays)
    code = code + generate_code_for_write_command(WriteCommand(IdentifierValue(VariableIdentifier('d'))), decl_vars, decl_arrays)
    code = code + generate_code_for_write_command(WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier(
        'arr', 'd'
    ))), decl_vars, decl_arrays)
    code = code + generate_code_for_write_command(WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier(
        'arr', IntNumberValue(-15)
    ))), decl_vars, decl_arrays)
    write_to_file('io_test.txt', code)


if __name__ == '__main__':
    test_write()
