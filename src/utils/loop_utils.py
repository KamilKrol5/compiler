from structures.AST import *
from utils.math_utils import *
from utils.label_provider import LabelProvider
from typing import Dict, Tuple
from utils.arrays_utils import *

''' Generates for loop'''


def generate_for_loop(loop: ForCommand) -> str:
    raise NotImplementedError()


''' Loads variable defined in identifier to dest_register (default is 0).
    If variable name is not present in the declared_variables dictionary an exception is raised'''


def load_value_by_identifier(identifier: Identifier, declared_variables: Dict[str, int], dest_register=0,
                             declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]] = {}) -> str:
    result: str = ''
    if isinstance(identifier, VariableIdentifier):
        if identifier.identifier_name not in declared_variables.keys():
            raise ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        result = f'LOAD {declared_variables[identifier.identifier_name]}\n'
    elif isinstance(identifier, ArrayElementByIntNumberIdentifier):
        if identifier.array_identifier not in declared_arrays.keys():
            raise ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        result = f'LOAD {compute_real_register_of_array_element(declared_arrays, identifier.array_identifier, identifier.index_value.value)}\n'
        # TODO
    elif isinstance(identifier, ArrayElementByVariableIdentifier):
        pass
        # TODO

    if dest_register != 0:
        result = result + f'STORE {dest_register}\n'
    return result


''' Generates code for subtraction left value from right value
    Registers used: 0-4'''


def generate_condition(condition: TwoValueCondition, declared_variables: Dict[str, int]) -> str:
    is_left_id_value = isinstance(condition.valueLeft, IdentifierValue)
    is_right_id_value = isinstance(condition.valueRight, IdentifierValue)
    # TODO handle array identifiers
    if not is_left_id_value and not is_right_id_value:
        left: int = condition.valueLeft.value
        right: int = condition.valueRight.value
        result = generate_number(right, destination_register=4)
        result = result + generate_number(left, destination_register=0) + 'SUB 4\n'
    elif not is_left_id_value and is_right_id_value:
        left: int = condition.valueLeft.value
        right: VariableIdentifier = condition.valueRight.identifier
        result = generate_number(left, destination_register=0) + f'SUB {declared_variables.get(right.identifier_name)}'
    elif is_left_id_value and not is_right_id_value:
        left: VariableIdentifier = condition.valueLeft.identifier
        right: int = condition.valueRight.value
        result = generate_number(right, destination_register=4) + \
            load_value_by_identifier(left, declared_variables, dest_register=0) + 'SUB 4'
    elif is_left_id_value and is_right_id_value:
        left: VariableIdentifier = condition.valueLeft.identifier
        right: VariableIdentifier = condition.valueRight.identifier
        result = load_value_by_identifier(left, declared_variables, dest_register=0) + \
            f'SUB {declared_variables.get(right.identifier_name)}'
    else:
        raise ValueError('Unknown instance of Identifier occurred.')
    return result
