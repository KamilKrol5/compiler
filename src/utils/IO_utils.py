from typing import Dict, Tuple

from utils.arrays_utils import compute_real_register_of_array_element, \
    generate_code_for_computing_index_of_array_element_by_variable
from utils.value_utils import generate_code_for_loading_value
from structures.ast.AST import ReadCommand, ArrayDeclaration, WriteCommand, VariableIdentifier, \
    ArrayElementByIntNumberIdentifier, ArrayElementByVariableIdentifier

''' Generates code for read command.'''


def generate_code_for_read_command(
        read_command: ReadCommand,
        declared_variables: Dict[str, int],
        declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]],
) -> str:
    if isinstance(read_command.identifier, VariableIdentifier):
        result: str = 'GET\n'
        result = result + f'STORE {declared_variables[read_command.identifier.identifier_name]}\n'
    elif isinstance(read_command.identifier, ArrayElementByIntNumberIdentifier):
        result: str = 'GET\n'
        real_element_index = compute_real_register_of_array_element(declared_arrays, read_command.identifier)
        result = result + f'STORE {real_element_index}\n'
    elif isinstance(read_command.identifier, ArrayElementByVariableIdentifier):
        index_computation: str = generate_code_for_computing_index_of_array_element_by_variable(
            read_command.identifier, declared_variables, declared_arrays)
        result: str = index_computation + f'STORE 1\nGET\nSTOREI 1\n'
    else:
        raise ValueError('Unknown instance of Identifier occurred.')
    return result


''' Generates code for write command.'''


def generate_code_for_write_command(
        write_command: WriteCommand,
        declared_variables: Dict[str, int],
        declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]],
) -> str:
    result: str = generate_code_for_loading_value(write_command.value, declared_variables, declared_arrays)
    return result + 'PUT\n'
