from structures.AST import *
from utils.math_utils import *
from utils.label_provider import LabelProvider
from typing import Dict, Tuple
from utils.arrays_utils import *

''' Generates for loop'''


def generate_for_loop(loop: ForCommand) -> str:
    raise NotImplementedError()


''' Loads variable defined in identifier to dest_register (default is 0).
    If variable name is not present in the declared_variables dictionary an exception is raised
    Registers used: 0-5'''


def load_value_by_identifier(identifier: Identifier, declared_variables: Dict[str, int], dest_register=0,
                             declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]] = {}) -> str:
    result: str = f'## load value by identifier begin\n'
    if isinstance(identifier, VariableIdentifier):
        if identifier.identifier_name not in declared_variables.keys():
            raise ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        result = result + f'LOAD {declared_variables[identifier.identifier_name]}\n'
    elif isinstance(identifier, ArrayElementByIntNumberIdentifier):
        if identifier.array_identifier not in declared_arrays.keys():
            raise ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        result = result + f'LOAD {compute_real_register_of_array_element(declared_arrays, identifier)}\n'
    elif isinstance(identifier, ArrayElementByVariableIdentifier):
        if identifier.array_identifier not in declared_arrays.keys():
            raise ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        if identifier.index_identifier not in declared_variables.keys():
            raise ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')

        result = result + generate_code_for_loading_array_element_by_variable(identifier, declared_variables,
                                                                              declared_arrays)

    if dest_register != 0:
        result = result + f'STORE {dest_register}\n'
    return result + f'## load value by identifier end\n'


''' Generates code for subtraction left value from right value
    Registers used: 0-4'''


def generate_condition(condition: TwoValueCondition, declared_variables: Dict[str, int],
                       declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]]) -> str:
    is_left_id_value = isinstance(condition.valueLeft, IdentifierValue)
    is_right_id_value = isinstance(condition.valueRight, IdentifierValue)
    # TODO handle array identifiers
    if not is_left_id_value and not is_right_id_value:
        left: int = condition.valueLeft.value
        right: int = condition.valueRight.value
        result = generate_number(right, destination_register=3)
        result = result + generate_number(left, destination_register=0) + 'SUB 3\n'
    elif not is_left_id_value and is_right_id_value:
        left: int = condition.valueLeft.value
        right: VariableIdentifier = condition.valueRight.identifier
        result = generate_number(left, destination_register=0) + \
            f'SUB {declared_variables.get(right.identifier_name)}\n'
    elif is_left_id_value and not is_right_id_value:
        left: VariableIdentifier = condition.valueLeft.identifier
        right: int = condition.valueRight.value
        result = generate_number(right, destination_register=3) + \
            load_value_by_identifier(left, declared_variables, dest_register=0, declared_arrays=declared_arrays) + \
            'SUB 3\n'
    elif is_left_id_value and is_right_id_value:
        left: VariableIdentifier = condition.valueLeft.identifier
        right: VariableIdentifier = condition.valueRight.identifier
        result = load_value_by_identifier(left, declared_variables, dest_register=3, declared_arrays=declared_arrays) +\
            load_value_by_identifier(right, declared_variables, dest_register=0, declared_arrays=declared_arrays) + \
            f'SUB 3\n'
    else:
        raise ValueError('Unknown instance of Identifier occurred.')
    return result
