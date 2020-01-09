from pprint import pprint
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter
from utils.expression_utils import generate_code_for_expression, ArrayDeclaration
from utils.math_utils import generate_number
from utils.test_utils import expected, get_numbers_from_run_code, flatten

decl_vars = {"c": 32, "d": 64}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}

interpreter = ASTInterpreter(Program(Declarations([]), Commands([])))
interpreter.declared_variables = decl_vars
interpreter.declared_arrays = decl_arrays


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


@expected(-58, 551, 557, -6)
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


if __name__ == '__main__':
    tests = [test_single_val_expr, test_add, test_sub]

    code_all = generate_number(555, 32) + generate_number(2, 64) + \
        generate_number(-2000, 125) + generate_number(-666, 142)

    expected = flatten(t.expected for t in tests)
    code_all = code_all + ''.join([t() for t in tests])
    returned: List[int] = get_numbers_from_run_code(code_all, 'expr_test.txt', 'exe_expr_test.txt')

    print('unmatched: (result number, (expected, returned))')
    pprint(list((i, (e, r)) for i, (e, r) in enumerate(zip(expected, returned)) if e != r))
    assert expected == returned
    print('ALL TESTS PASSED')
