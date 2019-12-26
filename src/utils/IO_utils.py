from utils.arrays_utils import *

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
    value = write_command.value
    if isinstance(value, IntNumberValue):
        return generate_number(value.value) + 'PUT\n'
    elif isinstance(value, IdentifierValue):
        if isinstance(value.identifier, VariableIdentifier):
            if value.identifier.identifier_name not in declared_variables.keys():
                ValueError('declared_variables dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            return f'LOAD {declared_variables[value.identifier.identifier_name]}\nPUT\n'
        elif isinstance(value.identifier, ArrayElementByIntNumberIdentifier):
            if value.identifier.array_identifier not in declared_arrays.keys():
                ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            return f'LOAD {compute_real_register_of_array_element(declared_arrays, value.identifier)}\nPUT\n'
        elif isinstance(value.identifier, ArrayElementByVariableIdentifier):
            if value.identifier.array_identifier not in declared_arrays.keys():
                ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            computation_of_index: str = generate_code_for_loading_array_element_by_variable(
                value.identifier, declared_variables, declared_arrays)
            return computation_of_index + 'PUT\n'
        else:
            raise ValueError('Unknown instance of Identifier occurred.')
    else:
        raise ValueError('Unknown instance of Value occurred.')
