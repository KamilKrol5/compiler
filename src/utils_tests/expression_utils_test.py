from structures.ast.AST import *
from utils.expression_utils import generate_code_for_expression, ArrayDeclaration
from utils.math_utils import generate_number
from utils.utils import write_to_file

decl_vars = {"c": 32, "d": 64}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}


# Expected: 111, 2, 555
def test_single_val_expr():
    code: str = generate_number(555, 32) + generate_number(2, 64) + generate_number(-2000, 125) + generate_number(
        -666,
        142)
    code = code + generate_code_for_expression(
        ExpressionHavingOneValue(IntNumberValue(111)), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingOneValue(
            IdentifierValue(VariableIdentifier('d'))), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingOneValue(
            IdentifierValue(VariableIdentifier('c'))), decl_vars, decl_arrays
    ) + 'PUT\n'
    write_to_file('expr_test.txt', code)


# Expected: -58, 551, 557, -6
def test_add():
    code: str = generate_number(555, 32) + generate_number(2, 64) + generate_number(-2000, 125) + generate_number(-666,
                                                                                                                  142)
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IntNumberValue(-60),
            'PLUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-4),
            IdentifierValue(VariableIdentifier('c')),
            'PLUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IdentifierValue(VariableIdentifier('c')),
            'PLUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(60),
            IntNumberValue(-66),
            'PLUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'

    write_to_file('expr_test.txt', code)


# Expected: 62, -559, -553, -126
def test_sub():
    code: str = generate_number(555, 32) + generate_number(2, 64) + generate_number(-2000, 125) + generate_number(-666,
                                                                                                                  142)
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IntNumberValue(-60),
            'MINUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-4),
            IdentifierValue(VariableIdentifier('c')),
            'MINUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IdentifierValue(VariableIdentifier('d')),
            IdentifierValue(VariableIdentifier('c')),
            'MINUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'
    code = code + generate_code_for_expression(
        ExpressionHavingTwoValues(
            IntNumberValue(-60),
            IntNumberValue(66),
            'MINUS'
        ), decl_vars, decl_arrays
    ) + 'PUT\n'

    write_to_file('expr_test.txt', code)


if __name__ == '__main__':
    test_sub()
