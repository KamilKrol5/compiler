from utils.loop_utils import *
from utils.loop_utils import *
from structures.AST import *


def test_arr_by_val(i=7):
    print(f'_______array by const value i={i}_______')
    arr = ArrayElementByIntNumberIdentifier('arr', IntNumberValue(i))
    res = load_value_by_identifier(arr, {}, 55, {'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-5),
                                                                                    IntNumberValue(10)))})
    print(res)
    assert res == f'LOAD {120+5+i}\nSTORE 55\n'


def test_val_val():
    print('_______val LE val_______')
    left = IntNumberValue(5)
    right = IntNumberValue(7)
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}))


def test_val_var():
    print('_______val LE var_______')
    left = IntNumberValue(5)
    right = IdentifierValue(VariableIdentifier('a'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}))


def test_var_val():
    print('_______var LE val_______')
    right = IntNumberValue(5)
    left = IdentifierValue(VariableIdentifier('a'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}))


def test_var_var():
    print('_______var LE var_______')
    left = IdentifierValue(VariableIdentifier('b'))
    right = IdentifierValue(VariableIdentifier('a'))
    cond = TwoValueCondition(left, right, 'LE')
    print(generate_condition(cond, {"a": 102, "b": 133}))


if __name__ == '__main__':
    test_val_val()
    test_var_val()
    test_val_var()
    test_var_var()
    test_arr_by_val()
    test_arr_by_val(0)
