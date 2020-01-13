from pprint import pprint
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter
from utils.test_utils import expected, get_numbers_from_run_code, flatten

program = Program(Declarations([
    NumberDeclaration('a'),
    NumberDeclaration('b'),
    NumberDeclaration('c'),
    NumberDeclaration('d'),
    NumberDeclaration('e'),
]), Commands([
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(1))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(-56))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(-8888888888))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(8888888888))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(213213))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(21))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(-1))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(32))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(3))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(38976541378465798465379864531))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(7698465))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(7698464))),
    AssignmentCommand(
        VariableIdentifier('a'),
        ExpressionHavingOneValue(IntNumberValue(7698420))),

]))
interpreter = ASTInterpreter(program)


@expected()
def init_variables() -> List[Command]:
    commands = [

    ]
    return commands


if __name__ == '__main__':
    tests = [init_variables, ]

    expected = flatten(t.expected for t in tests)
    interpreter.program.commands = Commands(flatten(t() for t in tests))
    code_all = program.accept(interpreter)
    returned: List[int] = get_numbers_from_run_code(code_all, 'performance_test.txt', 'exe_performance_test.txt')

    print('unmatched: (result number, (expected, returned))')
    pprint(list((i, (e, r)) for i, (e, r) in enumerate(zip(expected, returned)) if e != r))
    pprint(f'Expected: {expected}')
    pprint(f'Returned: {returned}')
    assert expected == returned
    print('ALL TESTS PASSED')
