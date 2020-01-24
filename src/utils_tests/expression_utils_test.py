from pprint import pprint
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter
from utils.IO_utils import generate_code_for_write_command
from utils.expression_utils import generate_code_for_expression
from utils.math_operations_code_generator import MathOperationsCodeGenerator
from utils.math_utils import generate_number, generate_abs, generate_numbers, generate_numbers_naive
from utils.test_utils import expected, get_numbers_from_run_code, flatten

decl_vars = {"c": 32, "d": 64, "e": 123, "f": 120, "g": 121, 'm_seven': 54, 'seven': 53, 'tw_four': 51, 'm_tw_four': 50,
             "one": 55, "zero": 56, "m_one": 57, "big_1": 58, "big_2": 59, "five": 60, "tw_eight": 61, 'hundred': 62,
             "m_five": 63, "m_tw_eight": 66, 'm_hundred': 65}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}

program = Program(Declarations([]), Commands([]))
interpreter = ASTInterpreter(program)
interpreter.constants = {1: 960, 2: 961, -8555: 962, 54211: 963, -4000: 964, 5: 965}
interpreter.declared_variables.update(decl_vars)
interpreter.declared_arrays.update(decl_arrays)


@expected(24, -24, -7, 7, 1, -1, 0, 5, -5, 28, -28, 100, -100, 10, 20, -15, -14, 10, 20)
def init() -> str:
    expr1 = ExpressionHavingOneValue(IntNumberValue(10))
    expr2 = ExpressionHavingOneValue(IntNumberValue(20))
    expr3 = ExpressionHavingOneValue(IntNumberValue(-15))
    expr4 = ExpressionHavingOneValue(IntNumberValue(-14))
    code: str = generate_numbers_naive(interpreter.constants)
    code = code + generate_code_for_expression(expr1, interpreter) + f'STORE {decl_arrays["arr"][0] + 5 }\n'  # arr[-15]=10
    code = code + generate_code_for_expression(expr2, interpreter) + f'STORE {decl_arrays["arr"][0] + 6 }\n'  # arr[-14]=20
    code = code + generate_code_for_expression(expr3, interpreter) + f'STORE {decl_vars["e"]}\n'  # e = -15
    code = code + generate_code_for_expression(expr4, interpreter) + f'STORE {decl_vars["f"]}\n'  # f = -14
    code = code + generate_code_for_expression(expr1, interpreter) + f'STORE {decl_vars["g"]}\n'  # g = 10
    code = code + generate_numbers({
        24: decl_vars['tw_four'],
        248974361532: decl_vars['big_1'],
        -879461521222224: decl_vars['big_2'],
        -24: decl_vars['m_tw_four'],
        -7: decl_vars['m_seven'],
        7: decl_vars['seven'],
        1: decl_vars['one'],
        -1: decl_vars['m_one'],
        0: decl_vars['zero'],
        5: decl_vars['five'],
        -5: decl_vars['m_five'],
        28: decl_vars['tw_eight'],
        -28: decl_vars['m_tw_eight'],
        100: decl_vars['hundred'],
        -100: decl_vars['m_hundred'], })
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('tw_four'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('m_tw_four'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('m_seven'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('seven'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('one'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('m_one'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('zero'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('five'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('m_five'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('tw_eight'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('m_tw_eight'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('hundred'))), interpreter)
    code = code + generate_code_for_write_command(
        WriteCommand(IdentifierValue(VariableIdentifier('m_hundred'))), interpreter)
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
    code: str = generate_number(1, destination_register=20)
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    code = code + cg.generate_code_for_load_ith_bit(decl_vars['g'], 20) + f'PUT\nLOAD 20\nINC\nSTORE 20\n'
    return code


@expected(0, 3, 5, 10, 4, 5, 6)
def test_log():
    cg = MathOperationsCodeGenerator(interpreter)
    code: str = generate_number(1, destination_register=255)
    code = code + generate_number(11, destination_register=500)
    code = code + generate_number(32, destination_register=520)
    code = code + generate_number(1024, destination_register=530)
    code = code + generate_number(24, destination_register=510)
    code = code + generate_number(63, destination_register=540)
    code = code + generate_number(65, destination_register=570)
    code = code + cg.generate_code_for_log(255, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(500, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(520, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(530, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(510, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(540, 15, 16) + f'PUT\n'
    code = code + cg.generate_code_for_log(570, 15, 16) + f'PUT\n'
    return code


@expected(156, 0, 32)
def test_abs():
    code: str = generate_number(-156, destination_register=510) + generate_abs(interpreter.label_provider) + 'PUT\n'
    code = code + generate_number(0, destination_register=500) + generate_abs(interpreter.label_provider) + 'PUT\n'
    code = code + generate_number(32, destination_register=520) + generate_abs(interpreter.label_provider) + 'PUT\n'
    return code


@expected(5000000000000000000000000000, 0)
def test_divide_big_numbers() -> str:
    code: str = generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(10000000000000000000000000000),
            IntNumberValue(2),
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
    return code


@expected(7, 0, 0, 2, 5, 0, 3, -4, -4, 3, 4, -37)
def test_divide_number_values() -> str:
    code: str = generate_code_for_expression(
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
            IntNumberValue(1),
            IntNumberValue(0),
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
            IntNumberValue(0),
            IntNumberValue(784),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(24),
            IntNumberValue(7),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(24),
            IntNumberValue(-7),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-24),
            IntNumberValue(7),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-24),
            IntNumberValue(-7),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-894),
            IntNumberValue(-215),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(7894),
            IntNumberValue(-215),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(2, 0, 3, -4, -4, 3, 0, 0, 0, 4, 0, -1, -1, 0, 5, 5, -6, -6, 5, 20, -20, -20, 20, 14, -1, -1, -4)
def test_divide_variables() -> str:
    code: str = generate_code_for_expression(
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
            IdentifierValue(VariableIdentifier('tw_four')),
            IdentifierValue(VariableIdentifier('seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_four')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_four')),
            IdentifierValue(VariableIdentifier('seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_four')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('one')),
            IdentifierValue(VariableIdentifier('zero')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('zero')),
            IdentifierValue(VariableIdentifier('one')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('zero')),
            IdentifierValue(VariableIdentifier('zero')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('five')),
            IdentifierValue(VariableIdentifier('seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('five')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_five')),
            IdentifierValue(VariableIdentifier('seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_five')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('five')),
            IdentifierValue(VariableIdentifier('one')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('m_five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            IdentifierValue(VariableIdentifier('five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            IdentifierValue(VariableIdentifier('m_five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('hundred')),
            IdentifierValue(VariableIdentifier('five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('hundred')),
            IdentifierValue(VariableIdentifier('m_five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_hundred')),
            IdentifierValue(VariableIdentifier('five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_hundred')),
            IdentifierValue(VariableIdentifier('m_five')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('hundred')),
            IdentifierValue(VariableIdentifier('seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('hundred')),
            IdentifierValue(VariableIdentifier('m_hundred')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_hundred')),
            IdentifierValue(VariableIdentifier('hundred')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(1, -1, -1, 1)
def test_divide_ones() -> str:
    code = generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('one')),
            IdentifierValue(VariableIdentifier('one')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('one')),
            IdentifierValue(VariableIdentifier('m_one')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_one')),
            IdentifierValue(VariableIdentifier('one')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_one')),
            IdentifierValue(VariableIdentifier('m_one')),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(0, 235740)
def test_modulo_big_numbers() -> str:
    code: str = generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(10000000000000000000000000000),
            IntNumberValue(0),
            'DIV'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(456988946138451327846351276843512),
            IntNumberValue(454562),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(0, 3, -4, 4, -3, 0, 0, 0, 0, 3, -2, 2, -3, 16, -12, 12, -16, 0, 0, 28, -72, 72, -28)
def test_modulo_variables() -> str:
    code: str = generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'f')),
            IdentifierValue(ArrayElementByVariableIdentifier('arr', 'e')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_four')),
            IdentifierValue(VariableIdentifier('seven')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_four')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_four')),
            IdentifierValue(VariableIdentifier('seven')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_four')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('one')),
            IdentifierValue(VariableIdentifier('one')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('one')),
            IdentifierValue(VariableIdentifier('zero')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('zero')),
            IdentifierValue(VariableIdentifier('one')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('zero')),
            IdentifierValue(VariableIdentifier('zero')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('five')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('m_five')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            IdentifierValue(VariableIdentifier('five')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            IdentifierValue(VariableIdentifier('m_five')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('hundred')),
            IdentifierValue(VariableIdentifier('tw_eight')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('hundred')),
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_hundred')),
            IdentifierValue(VariableIdentifier('tw_eight')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_hundred')),
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('m_seven')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('seven')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('hundred')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('tw_eight')),
            IdentifierValue(VariableIdentifier('m_hundred')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            IdentifierValue(VariableIdentifier('hundred')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('m_tw_eight')),
            IdentifierValue(VariableIdentifier('m_hundred')),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(6, 7, 5, 0, 0, 0, 3, -4, 4, -3, -61)
def test_modulo_number_values() -> str:
    code: str = generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(76),
            IntNumberValue(10),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(7),
            IntNumberValue(10),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(25),
            IntNumberValue(10),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(25),
            IntNumberValue(5),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(10000000000000000000000000000),
            IntNumberValue(0),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(0),
            IntNumberValue(784),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(24),
            IntNumberValue(7),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(24),
            IntNumberValue(-7),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-24),
            IntNumberValue(7),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-24),
            IntNumberValue(-7),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(7894),
            IntNumberValue(-215),
            'MOD'
        ), visitor=interpreter
    ) + 'PUT\n'
    return code


@expected(-95, 12, 1, 2, -8555, 54211, -4000, 5, 978455978546132456, 1, 1, 12)
def test_generate_number() -> str:
    code: str = generate_number(-95) + f'PUT\n'
    code = code + generate_number(12) + f'PUT\n'
    code = code + generate_number(1) + f'PUT\n'
    code = code + generate_number(2) + f'PUT\n'
    code = code + generate_number(-8555) + f'PUT\n'
    code = code + generate_number(54211) + f'PUT\n'
    code = code + generate_number(-4000) + f'PUT\n'
    code = code + generate_number(5) + f'PUT\n'
    code = code + generate_number(978455978546132456) + f'PUT\n'
    code = code + generate_number(1) + f'PUT\n'
    code = code + generate_number(1) + f'PUT\n'
    code = code + generate_number(12) + f'PUT\n'
    return code


if __name__ == '__main__':
    tests = [
        init,
        test_single_val_expr, test_add, test_sub, test_mul, test_taking_ith_bit, test_abs,
        test_divide_big_numbers,
        test_divide_number_values,
        test_divide_variables,
        test_divide_ones,
        test_log,
        test_modulo_big_numbers,
        test_modulo_number_values,
        test_modulo_variables,
        test_generate_number
    ]

    interpreter.generated_code.append(generate_number(555, destination_register=32) +
                                      generate_number(2, destination_register=64) +
                                      generate_number(-2000, destination_register=125) +
                                      generate_number(-666, destination_register=142))

    expected = flatten(t.expected for t in tests)
    interpreter.generated_code.append(''.join([t() for t in tests]))
    code_all = program.accept(interpreter)
    returned: List[int] = get_numbers_from_run_code(code_all, 'expr_test.txt', 'exe_expr_test.txt')
    pprint(f'Expected: {expected}', width=105)
    pprint(f'Returned: {returned}', width=105)
    print('unmatched: (result number, (expected, returned))')
    pprint(list((i, (e, r)) for i, (e, r) in enumerate(zip(expected, returned)) if e != r))
    assert expected == returned
    print('ALL TESTS PASSED')
