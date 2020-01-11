from utils.AST_interpreter import *
from utils.value_utils import load_value_by_identifier, generate_number


''' Generates code for subtraction left value from right value
    Registers used: 0-4'''


def generate_condition(condition: TwoValueCondition, visitor: 'ASTInterpreter') -> str:
    is_left_id_value = isinstance(condition.valueLeft, IdentifierValue)
    is_right_id_value = isinstance(condition.valueRight, IdentifierValue)

    if not is_left_id_value and not is_right_id_value:
        left: int = condition.valueLeft.value
        right: int = condition.valueRight.value
        result = generate_number(right, destination_register=3)
        result = result + generate_number(left, destination_register=0) + 'SUB 3\n'
    elif not is_left_id_value and is_right_id_value:
        left: int = condition.valueLeft.value
        right: VariableIdentifier = condition.valueRight.identifier
        result = generate_number(left, destination_register=0) + \
            f'SUB {visitor.declared_variables.get(right.identifier_name)}\n'
    elif is_left_id_value and not is_right_id_value:
        left: VariableIdentifier = condition.valueLeft.identifier
        right: int = condition.valueRight.value
        result = generate_number(right, destination_register=3) + \
            load_value_by_identifier(left, visitor, dest_register=0) + \
            'SUB 3\n'
    elif is_left_id_value and is_right_id_value:
        left: VariableIdentifier = condition.valueLeft.identifier
        right: VariableIdentifier = condition.valueRight.identifier
        result = load_value_by_identifier(right, visitor, dest_register=3) +\
            load_value_by_identifier(left, visitor, dest_register=0) + \
            f'SUB 3\n'
    else:
        raise ValueError('Unknown instance of Identifier occurred.')
    return result


def compare_values_knowing_registers(reg1: int, reg2: int) -> str:
    if reg1 == reg2:
        return 'SUB 0\n'
    result = ''
    if reg1 != 0:
        result = result + f'LOAD {reg1}\n'
    result = result + f'SUB {reg2}\n'
    return result
