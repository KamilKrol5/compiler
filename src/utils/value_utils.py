from typing import Tuple, Dict
from structures.ast.AST import Value, Identifier, ArrayDeclaration, VariableIdentifier, IntNumberValue, IdentifierValue, \
    ArrayElementByIntNumberIdentifier, ArrayElementByVariableIdentifier
from utils.arrays_utils import generate_code_for_loading_array_element_by_variable, \
    compute_real_register_of_array_element
from utils.math_utils import generate_number

''' Generates code for loading numeric value of Value object to the register 0 (p0).
    Each subclass of Value is supported.'''


def generate_code_for_loading_value(
        value: Value,
        declared_variables: Dict[str, int],
        declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]]
) -> str:
    if isinstance(value, IntNumberValue):
        return generate_number(value.value)
    elif isinstance(value, IdentifierValue):
        if isinstance(value.identifier, VariableIdentifier):
            if value.identifier.identifier_name not in declared_variables.keys():
                ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            return f'LOAD {declared_variables[value.identifier.identifier_name]}\n'
        elif isinstance(value.identifier, ArrayElementByIntNumberIdentifier):
            if value.identifier.array_identifier not in declared_arrays.keys():
                ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            return f'LOAD {compute_real_register_of_array_element(declared_arrays, value.identifier)}\n'
        elif isinstance(value.identifier, ArrayElementByVariableIdentifier):
            if value.identifier.array_identifier not in declared_arrays.keys():
                ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            loading_array_element: str = generate_code_for_loading_array_element_by_variable(
                value.identifier, declared_variables, declared_arrays)
            return loading_array_element
        else:
            raise ValueError('Unknown instance of Identifier occurred.')
    else:
        raise ValueError('Unknown instance of Value occurred.')


''' Computes register number where value of provided IdentifierValue is stored.
    Only VariableIdentifier and ArrayElementByIntNumberIdentifier is supported,
    because computation of register for ArrayElementByVariableIdentifier requires generating additional assembly code.
    If IdentifierValue having ArrayElementByVariableIdentifier as identifier is provided, then ValueError is raised.
    The purpose of this function is to provide an ability to perform computations on values without the need
    of loading to the register 0 (p0)'''


def compute_value_register(
        value: IdentifierValue,
        declared_variables: Dict[str, int],
        declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]]
) -> int:
    if isinstance(value.identifier, VariableIdentifier):
        if value.identifier.identifier_name not in declared_variables.keys():
            ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                       'write_command`s property - identifier. Variable might not be declared.')
        return declared_variables[value.identifier.identifier_name]
    elif isinstance(value.identifier, ArrayElementByIntNumberIdentifier):
        if value.identifier.array_identifier not in declared_arrays.keys():
            ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                       'write_command`s property - identifier. Variable might not be declared.')
        return compute_real_register_of_array_element(declared_arrays, value.identifier)
    elif isinstance(value.identifier, ArrayElementByVariableIdentifier):
        raise ValueError('Cannot compute register of value which identifier is ArrayElementByVariableIdentifier.'
                         'Separate assembly code needs to be created to do so.')
    else:
        raise ValueError('Unknown instance of Identifier occurred.')


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
