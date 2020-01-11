from pprint import pprint
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter
from utils.IO_utils import generate_code_for_write_command
from utils.expression_utils import generate_code_for_expression
from utils.math_operations_code_generator import MathOperationsCodeGenerator
from utils.math_utils import generate_number
from utils.test_utils import expected, get_numbers_from_run_code, flatten

decl_vars = {"c": 32, "d": 64, "e": 123, "f": 120, "g": 121}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}

program = Program(Declarations([]), Commands([]))
interpreter = ASTInterpreter(program)
interpreter.declared_variables.update(decl_vars)
interpreter.declared_arrays.update(decl_arrays)


@expected(10, 20, -15, -14, 10, 20)
def init() -> str:
    expr1 = ExpressionHavingOneValue(IntNumberValue(10))
    expr2 = ExpressionHavingOneValue(IntNumberValue(20))
    expr3 = ExpressionHavingOneValue(IntNumberValue(-15))
    expr4 = ExpressionHavingOneValue(IntNumberValue(-14))
    code: str = generate_code_for_expression(expr1, interpreter) + f'STORE {decl_arrays["arr"][0] + 5 }\n'  #arr[-15]=10
    code = code + generate_code_for_expression(expr2, interpreter) + f'STORE {decl_arrays["arr"][0] + 6 }\n'  #arr[-14]=20
    code = code + generate_code_for_expression(expr3, interpreter) + f'STORE {decl_vars["e"]}\n'  # e = -15
    code = code + generate_code_for_expression(expr4, interpreter) + f'STORE {decl_vars["f"]}\n'  # f = -14
    code = code + generate_code_for_expression(expr1, interpreter) + f'STORE {decl_vars["g"]}\n'  # g = 10
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15)))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-14)))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('e'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('f'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('arr', 'e'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('arr', 'f'))), interpreter)
    return code


@expected(111, 2, 555)
def test_single_val_expr():
    code: str = ''
    code = code + generate_code_for_expression(
        ExpressionHavingOneValue(IntNumberValue(111)), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingOneValue(
            IdentifierValue(VariableIdentifier('d'))), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingOneValue(
            IdentifierValue(VariableIdentifier('c'))), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(-58, 551, 557, -6, 30, 30)
def test_add():
    code: str = ''
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IntNumberValue(-60),
            'PLUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-4),
            IdentifierValue(VariableIdentifier('c')),
            'PLUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IdentifierValue(VariableIdentifier('c')),
            'PLUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(60),
            IntNumberValue(-66),
            'PLUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-14))),
            IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),
            'PLUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'e')),
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'f')),
            'PLUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(62, -559, -553, -126)
def test_sub():
    code: str = ''
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IntNumberValue(-60),
            'MINUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-4),
            IdentifierValue(VariableIdentifier('c')),
            'MINUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IdentifierValue(VariableIdentifier('c')),
            'MINUS'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-60),
            IntNumberValue(66),
            'MINUS'
        ), visitor=interpreter
    ) + 'PUT\n'

    return code


@expected(-120, -2220, 1110, -42, 42, 42, -42, 200, 200)
def test_mul():
    code: str = generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IntNumberValue(-60),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-4),
            IdentifierValue(VariableIdentifier('c')),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IdentifierValue(VariableIdentifier('c')),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(6),
            IntNumberValue(-7),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-6),
            IntNumberValue(-7),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(6),
            IntNumberValue(7),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-6),
            IntNumberValue(7),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-14))),
            IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'e')),
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'f')),
            'TIMES'
        ), visitor=interpreter
    ) + 'PUT\n'

    return code


@expected(0, 1, 0, 1, 0)
def test_taking_ith_bit():
    cg = MathOperationsCodeGenerator(interpreter)
    code: str = generate_number(1, 20)
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    return code


@expected(0, 3, 5, 10, 4, 5, 6)
def test_log():
    cg = MathOperationsCodeGenerator(interpreter)
    code: str = generate_number(1, 255)
    code = code + generate_number(11, 50)
    code = code + generate_number(32, 52)
    code = code + generate_number(1024, 53)
    code = code + generate_number(24, 51)
    code = code + generate_number(63, 54)
    code = code + generate_number(65, 57)
    code = code + cg.generate_code_for_log(255, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(50, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(52, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(53, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(51, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(54, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(57, 15, 16) + f'PUT\n'
    return code


@expected(7, 0, 2, 5, 5000000000000000000000000000, 2, 0, 0, 0)
def test_divide():
    code: str = ''
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(76),
            IntNumberValue(10),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(7),
            IntNumberValue(10),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(25),
            IntNumberValue(10),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(25),
            IntNumberValue(5),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(10000000000000000000000000000),
            IntNumberValue(2),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'f')),
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'e')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'e')),
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'f')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(10000000000000000000000000000),
            IntNumberValue(0),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(0),
            IntNumberValue(784),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


if __name__ == '__main__':
    tests = [
        init,
        test_single_val_expr, test_add, test_sub, test_mul, test_taking_ith_bit,
        test_divide,
        test_log
    ]

    interpreter.generated_code.append(generate_number(555, 32) + generate_number(2, 64) + \
                                      generate_number(-2000, 125) + generate_number(-666, 142))

    expected = flatten(t.expected for t in tests)
    interpreter.generated_code.append(''.join([t() for t in tests]))
    code_all = program.accept(interpreter)
    returned: List[int] = get_numbers_from_run_code(code_all, 'expr_test.txt', 'exe_expr_test.txt')
    pprint(f'Expected: {expected}')
    pprint(f'Returned: {returned}')
    print('unmatched: (result number, (expected, returned))')
    pprint(list((i, (e, r)) for i, (e, r) in enumerate(zip(expected, returned)) if e != r))
    assert expected == returned
    print('ALL TESTS PASSED')
