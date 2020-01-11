from pprint import pprint
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter
from utils.test_utils import expected, get_numbers_from_run_code, flatten

# a=10, b=-20, c=100, d=-120, e=0
# # brr[-20]=55
# # brr[-19]=44
# # brr[-10]=66
# # brr[0]=7
# # arr[10]=555
# # arr[11]=666
# # arr[25]=5
# # arr[20]=888
program = Program(Declarations([
    NumberDeclaration('a'),
    NumberDeclaration('b'),
    NumberDeclaration('c'),
    NumberDeclaration('d'),
    NumberDeclaration('e'),
    ArrayDeclaration('brr', IntNumberValue(-20), IntNumberValue(10)),
    ArrayDeclaration('arr', IntNumberValue(10), IntNumberValue(25)),
    ArrayDeclaration('crr', IntNumberValue(-4), IntNumberValue(2)),
]), Commands([]))
interpreter = ASTInterpreter(program)


@expected(10, -20, 100, -120, 0, 55, 44, 66, 7, 555, 666, 5, 888)
def init_variables() -> List[Command]:
    commands = [
        AssignmentCommand(
            VariableIdentifier('a'),
            ExpressionHavingOneValue(IntNumberValue(10))),
        WriteCommand(IdentifierValue(VariableIdentifier('a'))),
        AssignmentCommand(
            VariableIdentifier('b'),
            ExpressionHavingOneValue(IntNumberValue(-20))),
        WriteCommand(IdentifierValue(VariableIdentifier('b'))),
        AssignmentCommand(
            VariableIdentifier('c'),
            ExpressionHavingOneValue(IntNumberValue(100))),
        WriteCommand(IdentifierValue(VariableIdentifier('c'))),
        AssignmentCommand(
            VariableIdentifier('d'),
            ExpressionHavingOneValue(IntNumberValue(-120))),
        WriteCommand(IdentifierValue(VariableIdentifier('d'))),
        AssignmentCommand(
            VariableIdentifier('e'),
            ExpressionHavingOneValue(IntNumberValue(0))),
        WriteCommand(IdentifierValue(VariableIdentifier('e'))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('brr', IntNumberValue(-20)),
            ExpressionHavingOneValue(IntNumberValue(55))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(-20)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('brr', IntNumberValue(-19)),
            ExpressionHavingOneValue(IntNumberValue(44))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(-19)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('brr', IntNumberValue(-10)),
            ExpressionHavingOneValue(IntNumberValue(66))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(-10)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0)),
            ExpressionHavingOneValue(IntNumberValue(7))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('arr', IntNumberValue(10)),
            ExpressionHavingOneValue(IntNumberValue(555))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(10)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('arr', IntNumberValue(11)),
            ExpressionHavingOneValue(IntNumberValue(666))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(11)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('arr', IntNumberValue(25)),
            ExpressionHavingOneValue(IntNumberValue(5))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(25)))),
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('arr', IntNumberValue(20)),
            ExpressionHavingOneValue(IntNumberValue(888))),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(20)))),
    ]
    return commands


@expected(-1, 0, 1, 2, 3)
def test_for_write_i() -> List[Command]:
    return [
        ForCommand('i', IntNumberValue(-1), IntNumberValue(3), False, commands=Commands([
            WriteCommand(IdentifierValue((VariableIdentifier('i'))))
        ]))
    ]


@expected(-4, -5, -6, -7)
def test_for_write_i_down_to() -> List[Command]:
    return [
        ForCommand('i', IntNumberValue(-4), IntNumberValue(-7), is_down_to=True, commands=Commands([
            WriteCommand(IdentifierValue((VariableIdentifier('i'))))
        ]))
    ]


@expected(20, 29, 37, 44, 0)
def test_for_modify_end_and_start() -> List[Command]:
    return [
        ForCommand('i',  # 10 -> 7
                   IdentifierValue(VariableIdentifier('a')),
                   IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0))),
                   is_down_to=True,
                   commands=Commands([
                       AssignmentCommand(
                           ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0)),
                           ExpressionHavingOneValue(IntNumberValue(0))),
                       AssignmentCommand(
                           VariableIdentifier('a'),
                           ExpressionHavingTwoValues(
                               IdentifierValue(VariableIdentifier('i')), IdentifierValue(VariableIdentifier('a')),
                               'PLUS')),  # i + 10
                       WriteCommand(IdentifierValue((VariableIdentifier('a'))))
                   ])),
        WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0))))
    ]


@expected(15, 16, 14, 15, 13, 14)
def test_for_basic_nested() -> List[Command]:
    return [
        AssignmentCommand(
            ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0)),
            ExpressionHavingOneValue(IntNumberValue(7))),
        ForCommand('i',  # 9 -> 7
                   IntNumberValue(9),
                   IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0))),
                   is_down_to=True,
                   commands=Commands([
                       ForCommand('k',
                                  IntNumberValue(6),
                                  IdentifierValue(ArrayElementByIntNumberIdentifier('brr', IntNumberValue(0))),
                                  is_down_to=False,
                                  commands=Commands([
                                      AssignmentCommand(
                                          VariableIdentifier('e'),
                                          ExpressionHavingTwoValues(
                                              IdentifierValue(VariableIdentifier('i')),
                                              IdentifierValue(VariableIdentifier('k')),
                                              'PLUS')),  # k + i
                                      WriteCommand(IdentifierValue((VariableIdentifier('e'))))
                                  ]))
                   ])),
    ]


@expected(-10, -8, -6, -4, -10, -8, -6, -4, -10, -8, -6, -4, -10, -8, -6, -4, -128, 100, -120)
def test_for_nested_with_declared_iterator() -> List[Command]:
    return [
        AssignmentCommand(
            VariableIdentifier('e'),
            ExpressionHavingOneValue(IntNumberValue(0))),
        AssignmentCommand(
            VariableIdentifier('a'),
            ExpressionHavingOneValue(IntNumberValue(10))),
        ForCommand('c',  # 5 -> 8
                   IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(25))),
                   IntNumberValue(8),
                   is_down_to=False,
                   commands=Commands([
                       AssignmentCommand(
                           VariableIdentifier('a'),
                           ExpressionHavingTwoValues(
                               IdentifierValue(VariableIdentifier('d')),
                               IdentifierValue(VariableIdentifier('c')),
                               'MINUS')),
                       ForCommand('d',  # -5 -> -2
                                  IntNumberValue(-5),
                                  IntNumberValue(-2),
                                  is_down_to=False,
                                  commands=Commands([
                                      AssignmentCommand(
                                          VariableIdentifier('e'),
                                          ExpressionHavingTwoValues(
                                              IdentifierValue(VariableIdentifier('d')),
                                              IntNumberValue(2),
                                              'TIMES')),  # 2 * d
                                      WriteCommand(IdentifierValue((VariableIdentifier('e'))))
                                  ]))
                   ])),
        WriteCommand(IdentifierValue((VariableIdentifier('a')))),
        WriteCommand(IdentifierValue((VariableIdentifier('c')))),
        WriteCommand(IdentifierValue((VariableIdentifier('d'))))
    ]


@expected(100)
def test_for_no_iteration() -> List[Command]:
    return [
        AssignmentCommand(
            VariableIdentifier('e'),
            ExpressionHavingOneValue(IntNumberValue(0))),
        AssignmentCommand(
            VariableIdentifier('a'),
            ExpressionHavingOneValue(IntNumberValue(10))),
        ForCommand('c',  # 5 -> -58798798798789563218956316431
                   IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(25))),
                   IntNumberValue(-58798798798789563218956316431),
                   is_down_to=False,
                   commands=Commands([
                       WriteCommand(IdentifierValue((VariableIdentifier('e'))))
                   ])),
        ForCommand('e',  # 5 -> 57897695342312154231
                   IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(25))),
                   IntNumberValue(57897695342312154231),
                   is_down_to=True,
                   commands=Commands([
                       WriteCommand(IdentifierValue((VariableIdentifier('e'))))
                   ])),
        WriteCommand(IdentifierValue((VariableIdentifier('c'))))
    ]


@expected(-58798798798789563218956316431, -5879879879878956321895631643177777777777)
def test_for_one_iteration() -> List[Command]:
    return [
        ForCommand('c',  # -58798798798789563218956316431 -> -58798798798789563218956316431
                   IntNumberValue(-58798798798789563218956316431),
                   IntNumberValue(-58798798798789563218956316431),
                   is_down_to=False,
                   commands=Commands([
                       WriteCommand(IdentifierValue((VariableIdentifier('c'))))
                   ])),
        ForCommand('h',  # -58798798798789563218956316431 -> -58798798798789563218956316431
                   IntNumberValue(-5879879879878956321895631643177777777777),
                   IntNumberValue(-5879879879878956321895631643177777777777),
                   is_down_to=True,
                   commands=Commands([
                       WriteCommand(IdentifierValue((VariableIdentifier('h'))))
                   ])),
        # WriteCommand(IdentifierValue((VariableIdentifier('h')))) it should fail since there is no h here
    ]


@expected(310409881540927550055474295649559602537014075739180905267713380701381595716799736601)
def test_for_insane_multiplication() -> List[Command]:
    return [
        AssignmentCommand(
            VariableIdentifier('e'),
            ExpressionHavingOneValue(IntNumberValue(1))),
        ForCommand('a',  # 1 -> 10
                   IntNumberValue(1),
                   IntNumberValue(10),
                   is_down_to=False,
                   commands=Commands([
                       AssignmentCommand(
                           VariableIdentifier('e'),
                           ExpressionHavingTwoValues(
                               IdentifierValue(VariableIdentifier('e')),
                               IntNumberValue(223456789),
                               'TIMES')),  # e * this^
                   ])),
        WriteCommand(IdentifierValue((VariableIdentifier('e'))))
    ]


@expected(2, 1, 0, -1, -2, -3, -4)
def test_for_over_array() -> List[Command]:
    return [
        AssignmentCommand(
            VariableIdentifier('e'),
            ExpressionHavingOneValue(IntNumberValue(0))),
        AssignmentCommand(
            VariableIdentifier('a'),
            ExpressionHavingOneValue(IntNumberValue(10))),
        ForCommand('j',  # -4 -> 2
                   IntNumberValue(-4),
                   IntNumberValue(2),
                   is_down_to=False,
                   commands=Commands([
                       AssignmentCommand(
                           ArrayElementByVariableIdentifier('crr', 'j'),
                           ExpressionHavingOneValue(IdentifierValue(VariableIdentifier('j'))))
                   ])),
        ForCommand('ass',  # 2 -> -4
                   IntNumberValue(2),
                   IntNumberValue(-4),
                   is_down_to=True,
                   commands=Commands([
                       WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('crr', 'ass')))
                   ])),
    ]


if __name__ == '__main__':
    # a=10, b=-20, c=100, d=-120, e=0
    # brr[-20]=55
    # brr[-19]=44
    # brr[-10]=66
    # brr[0]=7
    # arr[10]=555
    # arr[11]=666
    # arr[25]=5
    # arr[20]=888
    tests = [init_variables, test_for_write_i, test_for_write_i_down_to, test_for_modify_end_and_start,
             test_for_basic_nested, test_for_nested_with_declared_iterator,
             test_for_no_iteration, test_for_one_iteration, test_for_insane_multiplication, test_for_over_array]

    expected = flatten(t.expected for t in tests)
    interpreter.program.commands = Commands(flatten(t() for t in tests))
    code_all = program.accept(interpreter)
    returned: List[int] = get_numbers_from_run_code(code_all, 'for_test.txt', 'exe_for_test.txt')

    print('unmatched: (result number, (expected, returned))')
    pprint(list((i, (e, r)) for i, (e, r) in enumerate(zip(expected, returned)) if e != r))
    pprint(f'Expected: {expected}')
    pprint(f'Returned: {returned}')
    assert expected == returned
    print('ALL TESTS PASSED')
