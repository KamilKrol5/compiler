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


# Expected <33>, 555, -2000, 2555, <22>, <11>, <-11>
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
                                    WriteCommand(IntNumberValue(-11))
                                ])
                            )
                        ])
                    )]))
        ]))
    return cond.accept(interpreter)


if __name__ == '__main__':
    code: str = generate_number(555, 32) + generate_number(2, 64) + generate_number(-2000, 125) + generate_number(
        -666,
        142)
    code = code + test_if_then_geq_ge_leq()
    write_to_file('../label_converter/command_test.txt', code)
