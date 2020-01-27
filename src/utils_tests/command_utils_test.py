from pprint import pprint
from utils.AST_interpreter import ASTInterpreter
from utils.test_utils import expected, flatten, get_numbers_from_run_code
from utils.math_utils import *
from structures.ast.AST import *
from typing import Tuple

decl_vars = {"c": 32, "d": 64, "array_var_one": 65, "array_var_two": 66, "i": 67}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}

# artificial variable creation
interpreter = ASTInterpreter(Program(Declarations([]), Commands([])))
interpreter.declared_variables = decl_vars
interpreter.declared_arrays = decl_arrays


@expected(1)
def test_if_then_neq() -> Tuple[Command]:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IntNumberValue(555), 'NEQ'),
        Commands(commands=[
            WriteCommand(IntNumberValue(1))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(1)
def test_if_then_eq() -> Tuple[Command]:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('c')), IntNumberValue(555), 'EQ'),
        Commands(commands=[
            WriteCommand(IntNumberValue(1))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(33, 22, 11)
def test_if_then_le_ge_eq() -> Tuple[Command]:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IntNumberValue(555), 'LE'),
        Commands(commands=[
            WriteCommand(IntNumberValue(33)),
            IfThenCommand(
                TwoValueCondition(
                    IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),  # -2000
                    IntNumberValue(-2001),
                    'GE'),
                Commands(commands=[
                    WriteCommand(IntNumberValue(22)),
                    IfThenCommand(
                        TwoValueCondition(IdentifierValue(VariableIdentifier('c')), IntNumberValue(555), 'EQ'),
                        Commands(commands=[
                            WriteCommand(IntNumberValue(11))
                        ])
                    )]))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(33, 22)
def test_if_then_leq_geq_neq() -> Tuple[Command]:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IntNumberValue(555), 'LEQ'),
        Commands(commands=[
            WriteCommand(IntNumberValue(33)),
            IfThenCommand(
                TwoValueCondition(
                    IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),  # -2000
                    IntNumberValue(-2001),
                    'GEQ'),
                Commands(commands=[
                    WriteCommand(IntNumberValue(22)),
                    IfThenCommand(
                        TwoValueCondition(IdentifierValue(VariableIdentifier('c')), IntNumberValue(555), 'NEQ'),
                        Commands(commands=[
                            WriteCommand(IntNumberValue(11))
                        ])
                    )]))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(33, 555, -2000, 22, 11, 111)
def test_if_then_geq_ge_leq() -> Tuple[Command]:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IdentifierValue(VariableIdentifier('d')), 'GEQ'),
        Commands(commands=[
            WriteCommand(IntNumberValue(33)),
            WriteCommand(IdentifierValue(VariableIdentifier('c'))),
            WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15)))),
            IfThenCommand(
                TwoValueCondition(
                    IdentifierValue(VariableIdentifier('c')),
                    IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),  # -2000
                    'GE'),
                Commands(commands=[
                    WriteCommand(IntNumberValue(22)),
                    IfThenCommand(
                        TwoValueCondition(IntNumberValue(2), IdentifierValue(VariableIdentifier('d')), 'LEQ'),
                        Commands(commands=[
                            WriteCommand(IntNumberValue(11)),
                            IfThenCommand(
                                TwoValueCondition(IntNumberValue(2), IdentifierValue(VariableIdentifier('d')), 'GEQ'),
                                Commands(commands=[
                                    WriteCommand(IntNumberValue(111))
                                ])
                            )
                        ])
                    )]))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(44, 555, 1000, -2000)
def test_if_then_else_neq_on_false() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IdentifierValue(VariableIdentifier('d')),
                                    'NEQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(-33)),
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(44)),
            WriteCommand(IdentifierValue(VariableIdentifier('c'))),
            WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd'))),
            WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15)))),
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(33)
def test_if_then_else_neg_on_true() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(VariableIdentifier('c')), IdentifierValue(VariableIdentifier('d')),
                                    'NEQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(33)),
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(-44)),
            WriteCommand(IdentifierValue(VariableIdentifier('c'))),
            WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd'))),
            WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15)))),
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(44, 1000, 555, -2000)
def test_if_then_else_eq_on_false() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),  # 1000 == 2
                                    IdentifierValue(VariableIdentifier('d')),
                                    'EQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(-11)),
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(44)),
            WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd'))),
            WriteCommand(IdentifierValue(VariableIdentifier('c'))),
            WriteCommand(IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15)))),
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(11, 1000)
def test_if_then_else_eq_on_true() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),  # 1000 == 1000
                                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                                    'EQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(11)),
            WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd'))),
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(-44))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(100, 200)
def test_if_then_else_le_on_true_ge_on_false() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(VariableIdentifier('d')),  # 2 < 1000
                                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                                    'LE'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(100)),
            IfThenElseCommand(
                condition=TwoValueCondition(
                    # 555 > 1000
                    IdentifierValue(VariableIdentifier('c')),
                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                    'GE'),
                commands_true=Commands(commands=[
                    WriteCommand(IntNumberValue(-44)),
                ]),
                commands_false=Commands(commands=[
                    WriteCommand(IntNumberValue(200))
                ]))
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(-44))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(200, 300)
def test_if_then_else_le_on_false_ge_on_true() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(VariableIdentifier('d')),  # 2 < -2000
                                    IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),
                                    'LE'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(-44))
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(200)),
            IfThenElseCommand(
                condition=TwoValueCondition(
                    # 1000 > 555
                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                    IdentifierValue(VariableIdentifier('c')),
                    'GE'),
                commands_true=Commands(commands=[
                    WriteCommand(IntNumberValue(300)),
                ]),
                commands_false=Commands(commands=[
                    WriteCommand(IntNumberValue(-44))
                ]))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(100, 200)
def test_if_then_else_leq_on_true_geq_on_false() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(VariableIdentifier('d')),  # 2 <= 1000
                                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                                    'LEQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(100)),
            IfThenElseCommand(
                condition=TwoValueCondition(
                    # 555 >= 1000
                    IdentifierValue(VariableIdentifier('c')),
                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                    'GEQ'),
                commands_true=Commands(commands=[
                    WriteCommand(IntNumberValue(-44)),
                ]),
                commands_false=Commands(commands=[
                    WriteCommand(IntNumberValue(200))
                ]))
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(-44))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(100, 200)
def test_if_then_else_leq_on_true_geq_on_true_with_equality() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(  # 1000 <= 1000
            IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
            IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
            'LEQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(100)),
            IfThenElseCommand(
                condition=TwoValueCondition(
                    # 555 >= 555
                    IdentifierValue(VariableIdentifier('c')),
                    IdentifierValue(VariableIdentifier('c')),
                    'GEQ'),
                commands_true=Commands(commands=[
                    WriteCommand(IntNumberValue(200)),
                ]),
                commands_false=Commands(commands=[
                    WriteCommand(IntNumberValue(-44))
                ]))
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(-44))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(200, 300)
def test_if_then_else_leq_on_false_geq_on_true() -> Tuple[Command]:
    cond = IfThenElseCommand(
        condition=TwoValueCondition(IdentifierValue(VariableIdentifier('d')),  # 2 <= -2000
                                    IdentifierValue(ArrayElementByIntNumberIdentifier('arr', IntNumberValue(-15))),
                                    'LEQ'),
        commands_true=Commands(commands=[
            WriteCommand(IntNumberValue(-44))
        ]),
        commands_false=Commands(commands=[
            WriteCommand(IntNumberValue(200)),
            IfThenElseCommand(
                condition=TwoValueCondition(
                    # 1000 >= 1000
                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                    IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd')),
                    'GEQ'),
                commands_true=Commands(commands=[
                    WriteCommand(IntNumberValue(300)),
                ]),
                commands_false=Commands(commands=[
                    WriteCommand(IntNumberValue(-44))
                ]))
        ]))
    # cond.accept(interpreter)
    return cond,


@expected(0, 0)
def test_while_do_zero_iterations() -> Tuple[Command, Command, Command]:
    loop = WhileDoCommand(condition=TwoValueCondition(
        IdentifierValue(VariableIdentifier('i')),
        IdentifierValue(VariableIdentifier('array_var_two')),
        'LEQ'),  # i <= -10 (i=0)
        commands=Commands([  # i = i PLUS 1
            AssignmentCommand(
                VariableIdentifier('i'),
                ExpressionHavingTwoValues(IdentifierValue(VariableIdentifier('i')), IntNumberValue(1), 'PLUS'))
        ]))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    # write.accept(interpreter)
    # loop.accept(interpreter)
    # write.accept(interpreter)
    return write, loop, write


@expected(0, 50)
def test_while_do_50_iterations() -> Tuple[Command, Command, Command]:
    loop = WhileDoCommand(condition=TwoValueCondition(
        IdentifierValue(VariableIdentifier('i')),
        IdentifierValue(VariableIdentifier('array_var_one')),
        'LE'),  # i <= 50 (i=0)
        commands=Commands([  # i = i PLUS 1
            AssignmentCommand(
                VariableIdentifier('i'),
                ExpressionHavingTwoValues(IdentifierValue(VariableIdentifier('i')), IntNumberValue(1), 'PLUS'))
        ]))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    # loop.accept(interpreter)
    # write.accept(interpreter)
    return write, loop, write


@expected(555, 1000, 1000, 1000, 555, 555, 6, -80)
def test_while_do_nested() -> Tuple[Command, Command, Command, Command]:
    zero = AssignmentCommand(
        VariableIdentifier('i'),
        ExpressionHavingOneValue(IntNumberValue(0)))
    loop = WhileDoCommand(condition=TwoValueCondition(
        IdentifierValue(VariableIdentifier('i')),
        IntNumberValue(6),
        'NEQ'),  # i != 6 (i=0)
        commands=Commands([  # i = i PLUS 1
            WriteCommand(IdentifierValue(VariableIdentifier('c'))),
            AssignmentCommand(
                VariableIdentifier('i'),
                ExpressionHavingTwoValues(IdentifierValue(VariableIdentifier('i')), IntNumberValue(1), 'PLUS')),
            WhileDoCommand(condition=TwoValueCondition(  # 3 times
                IdentifierValue(VariableIdentifier('i')),
                IntNumberValue(4),
                'LE'),
                commands=Commands([
                    WriteCommand(IdentifierValue(ArrayElementByVariableIdentifier('brr', 'd'))),
                    AssignmentCommand(  # array_var_two = array_var_two - array_var_two
                        VariableIdentifier('array_var_two'),
                        ExpressionHavingTwoValues(
                            IdentifierValue(VariableIdentifier('array_var_two')),
                            IdentifierValue(VariableIdentifier('array_var_two')), 'PLUS')),
                    AssignmentCommand(
                        VariableIdentifier('i'),
                        ExpressionHavingTwoValues(IdentifierValue(VariableIdentifier('i')), IntNumberValue(1), 'PLUS')),
                ]))

        ]))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    write2 = WriteCommand(IdentifierValue(VariableIdentifier('array_var_two')))
    # loop.accept(interpreter)
    # write.accept(interpreter)
    return zero, loop, write, write2


@expected(50)
def test_do_while_50_iterations() -> Tuple[Command, Command, Command]:
    zero = AssignmentCommand(
        VariableIdentifier('i'),
        ExpressionHavingOneValue(IntNumberValue(0)))
    loop = DoWhileCommand(condition=TwoValueCondition(
        IdentifierValue(VariableIdentifier('i')),
        IdentifierValue(VariableIdentifier('array_var_one')),
        'LE'),  # i <= 50 (i=0)
        commands=Commands([  # i = i PLUS 1
            AssignmentCommand(
                VariableIdentifier('i'),
                ExpressionHavingTwoValues(IdentifierValue(VariableIdentifier('i')), IntNumberValue(1), 'PLUS'))
        ]))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    # loop.accept(interpreter)
    # write.accept(interpreter)
    return zero, loop, write


@expected(0, 1)
def test_do_while_zero_iterations() -> Tuple[Command, Command, Command, Command]:
    zero = AssignmentCommand(
        VariableIdentifier('i'),
        ExpressionHavingOneValue(IntNumberValue(0)))
    loop = DoWhileCommand(condition=TwoValueCondition(
        IdentifierValue(VariableIdentifier('i')),
        IntNumberValue(-10),
        'LEQ'),  # i <= -10 (i=0)
        commands=Commands([  # i = i PLUS 1
            AssignmentCommand(
                VariableIdentifier('i'),
                ExpressionHavingTwoValues(IdentifierValue(VariableIdentifier('i')), IntNumberValue(1), 'PLUS'))
        ]))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    # write.accept(interpreter)
    # loop.accept(interpreter)
    # write.accept(interpreter)
    return zero, write, loop, write


@expected(10, 11)
def test_increment_decrement_command_inc() -> Tuple[Command, Command, Command, Command]:
    assign_i = AssignmentCommand(
        VariableIdentifier('i'),
        ExpressionHavingOneValue(IntNumberValue(10)))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    inc_dec_command = IncrementDecrementCommand(VariableIdentifier('i'))
    return assign_i, write, inc_dec_command, write


@expected(5, 4)
def test_increment_decrement_command_dec() -> Tuple[Command, Command, Command, Command]:
    assign_i = AssignmentCommand(
        VariableIdentifier('i'),
        ExpressionHavingOneValue(IntNumberValue(5)))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    inc_dec_command = IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=True)
    return assign_i, write, inc_dec_command, write


@expected(5)
def test_increment_decrement_command_multiple() -> Tuple[Command, Command, Command]:
    assign_i = AssignmentCommand(
        VariableIdentifier('i'),
        ExpressionHavingOneValue(IntNumberValue(5)))
    write = WriteCommand(IdentifierValue(VariableIdentifier('i')))
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IntNumberValue(555), 'NEQ'), # true
        Commands(commands=[
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=True),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=False),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=True),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=False),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=False),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=False),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=True),
            IncrementDecrementCommand(VariableIdentifier('i'), is_decrement=True),
        ]))
    return assign_i, cond, write


if __name__ == '__main__':
    code_generating_constants: str = generate_number(555, {}, 32) + generate_number(2, {}, 64) + generate_number(-2000, {}, 125) + \
                                     generate_number(-666, {}, 142) + generate_number(1000, {}, 263) + generate_number(50, {}, 65) +\
                                     generate_number(-10, {}, 66) + \
                                     generate_number(0, {}, 67)
    # c = 555, d = 2, arr[-15] = -2000, brr[2] =  brr[d] = 1000, array_var_one = 50, array_var_two = -10, i = 0
    interpreter.generated_code.append(code_generating_constants)
    program1 = Program(Declarations([]), Commands([
        *test_do_while_zero_iterations()
    ]))
    code = interpreter.visit_program(program1)
    # returned1: List[int] = get_numbers_from_run_code(code, 'command_test.txt', 'exe_command_test.txt')

    interpreter.generated_code.clear()
    interpreter.generated_code.append(code_generating_constants)
    tests = [
        test_if_then_eq, test_if_then_neq, test_if_then_geq_ge_leq,
        test_if_then_leq_geq_neq, test_if_then_le_ge_eq, test_if_then_else_eq_on_false,
        test_if_then_else_eq_on_true, test_if_then_else_neg_on_true, test_if_then_else_neq_on_false,
        test_if_then_else_le_on_false_ge_on_true, test_if_then_else_le_on_true_ge_on_false,
        test_if_then_else_leq_on_false_geq_on_true, test_if_then_else_leq_on_true_geq_on_false,
        test_if_then_else_leq_on_true_geq_on_true_with_equality, test_while_do_zero_iterations,
        test_while_do_50_iterations, test_while_do_nested, test_do_while_50_iterations,
        test_do_while_zero_iterations, test_increment_decrement_command_inc, test_increment_decrement_command_dec,
        test_increment_decrement_command_multiple]

    expected = flatten(t.expected for t in tests)

    program1 = Program(Declarations([]), Commands(flatten(t() for t in tests)))
    # 1, 1, <33>, 555, -2000, <22>, <11>, <111>, 33, 22, 33, 22, 11, 44, 1000, 555, -2000, 11, 1000,
    # <33>, 44, 555, 1000, -2000, 200, 300,  100, 200,  200, 300,  100, 200, 100, 200,
    # 0, 0, 0, 50 (while do) 555, 1000, 1000, 1000, 555, 555, 6, -80 (while do nested),
    # 50, 0, 1 (do while), 10, 11, 5, 4

    code_all: str = interpreter.visit_program(program1)
    returned: List[int] = get_numbers_from_run_code(code_all, 'command_test_all.txt',
                                                    should_save_intermediate_code=True)

    print('unmatched: (result number, (expected, returned))')
    pprint(list((i, (e, r)) for i, (e, r) in enumerate(zip(expected, returned)) if e != r))
    assert expected == returned
    print('ALL TESTS PASSED')
