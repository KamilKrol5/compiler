from utils.AST_interpreter import ASTInterpreter
from utils.utils import write_to_file
from utils.math_utils import *
from structures.ast.AST import *

decl_vars = {"c": 32, "d": 64}
decl_arrays = {
    'arr': (120, 135, ArrayDeclaration('arr', IntNumberValue(-20), IntNumberValue(15))),
    'brr': (256, 266, ArrayDeclaration('brr', IntNumberValue(-5), IntNumberValue(5)))}

# artificial variable creation
interpreter = ASTInterpreter(Program(Declarations([]), Commands([])))
interpreter.declared_variables = decl_vars
interpreter.declared_arrays = decl_arrays


# Expected 1
def test_if_then_neq() -> str:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('d')), IntNumberValue(555), 'NEQ'),
        Commands(commands=[
            WriteCommand(IntNumberValue(1))
        ]))
    return cond.accept(interpreter)


# Expected 1
def test_if_then_eq() -> str:
    cond = IfThenCommand(
        TwoValueCondition(IdentifierValue(VariableIdentifier('c')), IntNumberValue(555), 'EQ'),
        Commands(commands=[
            WriteCommand(IntNumberValue(1))
        ]))
    return cond.accept(interpreter)


# Expected 33, 22, 11
def test_if_then_le_ge_eq() -> str:
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
    return cond.accept(interpreter)


# Expected 33, 22
def test_if_then_leq_geq_neq() -> str:
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
    return cond.accept(interpreter)


# Expected <33>, 555, -2000, 2555, <22>, <11>, <111>
def test_if_then_geq_ge_leq() -> str:
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
    return cond.accept(interpreter)


# Expected 44, 555, 1000, -2000
def test_if_then_else_neq_on_false() -> str:
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
    return cond.accept(interpreter)


# Expected: <33>
def test_if_then_else_neg_on_true() -> str:
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
    return cond.accept(interpreter)


# Expected: 44, 1000, 555, -2000
def test_if_then_else_eq_on_false() -> str:
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
    return cond.accept(interpreter)


# Expected: 11, 1000
def test_if_then_else_eq_on_true() -> str:
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
    return cond.accept(interpreter)


# Expected: 100, 200
def test_if_then_else_le_on_true_ge_on_false() -> str:
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
    return cond.accept(interpreter)


# Expected: 200, 300
def test_if_then_else_le_on_false_ge_on_true() -> str:
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
    return cond.accept(interpreter)


# Expected: 100, 200
def test_if_then_else_leq_on_true_geq_on_false() -> str:
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
    return cond.accept(interpreter)


# Expected: 100, 200
def test_if_then_else_leq_on_true_geq_on_true_with_equality() -> str:
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
    return cond.accept(interpreter)


# Expected: 200, 300
def test_if_then_else_leq_on_false_geq_on_true() -> str:
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
    return cond.accept(interpreter)


if __name__ == '__main__':
    code_generating_constants: str = generate_number(555, 32) + generate_number(2, 64) + generate_number(-2000, 125) + \
        generate_number(-666, 142) + generate_number(1000, 263)
    # c = 555, d = 2, arr[-15] = -2000, brr[2] =  brr[d] = 1000
    code = code_generating_constants + \
        test_if_then_else_leq_on_false_geq_on_true() \
        + test_if_then_else_leq_on_true_geq_on_false() \
        + test_if_then_else_leq_on_true_geq_on_true_with_equality()
    write_to_file('../label_converter/command_test.txt', code)

    # 1, 1, <33>, 555, -2000, 2555, <22>, <11>, <111>, 33, 22, 33, 22, 11, 44, 1000, 555, -2000, 11, 1000,
    # <33>, 44, 555, 1000, -2000, 200, 300,  100, 200,  200, 300,  100, 200, 100, 200
    code_all = code_generating_constants + test_if_then_eq() + test_if_then_neq() + test_if_then_geq_ge_leq() + \
        test_if_then_leq_geq_neq() + test_if_then_le_ge_eq() + test_if_then_else_eq_on_false() + \
        test_if_then_else_eq_on_true() + test_if_then_else_neg_on_true() + test_if_then_else_neq_on_false() + \
        test_if_then_else_le_on_false_ge_on_true() + test_if_then_else_le_on_true_ge_on_false() + \
        test_if_then_else_leq_on_false_geq_on_true() \
        + test_if_then_else_leq_on_true_geq_on_false() \
        + test_if_then_else_leq_on_true_geq_on_true_with_equality()
    write_to_file('../label_converter/command_test_all.txt', code_all)

    import subprocess as subpr

    # out = subpr.check_output(["C:\\Users\\Kamil\\compiler\\maszyna_wirtualna\\maszyna-wirtualna",
    #                           "C:\\Users\\Kamil\\compiler\\src\\label_converter"])
    # print(out)
