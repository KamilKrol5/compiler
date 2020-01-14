from utils.AST_interpreter import *
from utils.arrays_utils import compute_real_register_of_array_element, \
    generate_code_for_computing_index_of_array_element_by_variable
from utils.compilation_exceptions import AnAttemptToModifyCounterException
from utils.value_utils import generate_code_for_loading_value
from structures.ast.AST import ReadCommand, WriteCommand, VariableIdentifier, \
    ArrayElementByIntNumberIdentifier, ArrayElementByVariableIdentifier

''' Generates code for read command.'''


def generate_code_for_read_command(
        read_command: ReadCommand,
        visitor: 'ASTInterpreter',
) -> str:
    if isinstance(read_command.identifier, VariableIdentifier):
        if read_command.identifier.identifier_name not in visitor.declared_variables:
            raise UndeclaredVariableException(f"Undeclared variable '{read_command.identifier.identifier_name}'.",
                                              occurrence_place=read_command.identifier.start_position)
        if read_command.identifier.identifier_name in visitor.local_variables:
            raise AnAttemptToModifyCounterException(
                f"An attempt to modify iterator: '{read_command.identifier.identifier_name}'.",
                occurrence_place=read_command.start_position)
        result: str = 'GET\n'
        result = result + f'STORE {visitor.declared_variables[read_command.identifier.identifier_name]}\n'
    elif isinstance(read_command.identifier, ArrayElementByIntNumberIdentifier):
        arr_name = read_command.identifier.array_identifier
        if arr_name not in visitor.declared_arrays:
            raise UndeclaredArrayException(
                f"An array '{arr_name}' is not declared.", occurrence_place=read_command.identifier.start_position)
        result: str = 'GET\n'
        real_element_index = compute_real_register_of_array_element(visitor.declared_arrays, read_command.identifier)
        result = result + f'STORE {real_element_index}\n'
    elif isinstance(read_command.identifier, ArrayElementByVariableIdentifier):
        arr_name = read_command.identifier.array_identifier
        var = read_command.identifier.index_identifier
        if arr_name not in visitor.declared_arrays:
            raise UndeclaredArrayException(
                f"An array '{arr_name}' is not declared.", occurrence_place=read_command.identifier.start_position)
        if var not in visitor.declared_variables:
            raise UndeclaredVariableException(
                f"An index variable for accessing element of array '{arr_name}'('{var}') is not declared."
                f" '{var}' is not declared",
                occurrence_place=read_command.identifier.start_position)
        index_computation: str = generate_code_for_computing_index_of_array_element_by_variable(
            read_command.identifier, visitor)
        result: str = index_computation + f'STORE 1\nGET\nSTOREI 1\n'
    else:
        raise ValueError('Unknown instance of Identifier occurred.')
    return result


''' Generates code for write command.'''


def generate_code_for_write_command(
        write_command: WriteCommand,
        visitor: 'ASTInterpreter'
) -> str:
    result: str = '## BEGIN write command\n' + \
        generate_code_for_loading_value(write_command.value, visitor)
    return result + 'PUT\n' + '## END write command\n'
