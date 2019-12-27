from utils.loop_utils import *
from utils.loop_utils import *
from structures.AST import *


def test_arr_by_val(i=7):
    print(f'_______array by const value i={i}_______')
    arr = ArrayElementByIntNumberIdentifier('arr', IntNumberValue(i))
    res = load_value_by_identifier(arr, {}, 55, {'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-5),
                                                                                    IntNumberValue(10)))})
    print(res)
    assert res == f'## load value by identifier begin\nLOAD {120 + 5 + i}\nSTORE 55\n## load value by identifier end\n'


def test_arr_by_var():
    print(f'_______array by declared variable_______')
    arr = ArrayElementByVariableIdentifier('arr', 'b')
    res = load_value_by_identifier(arr, {'b': 32}, 55, {'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20),
                                                                                           IntNumberValue(15)))})
    print(res)
    assert res == '## load value by identifier begin\nSUB 0\nINC\nSTORE 1\nDEC\nINC\nSHIFT 1\nINC\nSHIFT 1\nINC\n' \
                  'SHIFT 1\nINC\nSHIFT 1\nSHIFT 1\nSHIFT 1\nSTORE 5\nSUB 0\nINC\nSTORE 1\nDEC\nINC\nSHIFT 1\nSHIFT 1' \
                  '\nINC\nSHIFT 1\nSHIFT 1\nSTORE 1\nSUB 0\nSUB 1\nSTORE 4\nLOAD 32\nSUB 4\nADD 5\nLOADI 0\nSTORE 55\n'\
                  '## load value by identifier end\n'


def test_val_val():
    print('_______val LE val_______')
    left = IntNumberValue(5)
    right = IntNumberValue(7)
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}, declared_arrays={}))


def test_val_var():
    print('_______val LE var_______')
    left = IntNumberValue(5)
    right = IdentifierValue(VariableIdentifier('a'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}, declared_arrays={}))


def test_var_val():
    print('_______var LE val_______')
    right = IntNumberValue(5)
    left = IdentifierValue(VariableIdentifier('a'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}, declared_arrays={}))


def test_var_var():
    print('_______var LE var_______')
    left = IdentifierValue(VariableIdentifier('b'))
    right = IdentifierValue(VariableIdentifier('a'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}, declared_arrays={}))


def test_arr_by_var_arr_by_var():
    print('_______var LE var_______')
    left = IdentifierValue(ArrayElementByVariableIdentifier('brr', 'c'))
    right = IdentifierValue(ArrayElementByVariableIdentifier('arr', 'c'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"c": 32, "d": 64},
                             declared_arrays={'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20),
                                                                                 IntNumberValue(15))), 'brr': (
                                 256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}))


def test_arr_by_var_arr_by_val():
    print('_______var LE var_______')
    left = IdentifierValue(ArrayElementByVariableIdentifier('brr', 'c'))
    right = IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(11)))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"c": 32, "d": 64},
                             declared_arrays={'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20),
                                                                                 IntNumberValue(15))), 'brr': (
                                 256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}))


def test_arr_by_val_arr_by_var():
    print('_______var LE var_______')
    left = IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(3)))
    right = IdentifierValue(ArrayElementByVariableIdentifier('arr', 'c'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"c": 32, "d": 64},
                             declared_arrays={'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20),
                                                                                 IntNumberValue(15))), 'brr': (
                                 256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}))


def test_arr_by_val_arr_by_val():
    print('_______var LE var_______')
    left = IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(3)))
    right = IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(7)))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"c": 32, "d": 64},
                             declared_arrays={'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20),
                                                                                 IntNumberValue(15))), 'brr': (
                                 256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}))


if __name__ == '__main__':
    test_val_val()
    test_var_val()
    test_val_var()
    test_var_var()
    test_arr_by_val()
    test_arr_by_val(0)
    test_arr_by_var()
    test_arr_by_var_arr_by_var()
    test_arr_by_val_arr_by_var()
    test_arr_by_val_arr_by_val()
    test_arr_by_var_arr_by_val()