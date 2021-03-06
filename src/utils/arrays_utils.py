from utils.AST_interpreter import *
from utils.compilation_exceptions import *
from utils.math_utils import generate_number
from typing import Dict, Tuple
from structures.ast.AST import ArrayDeclaration, ArrayElementByIntNumberIdentifier, ArrayElementByVariableIdentifier


def compute_relative_register_of_array_element(declaration: ArrayDeclaration, user_typed_element_index: int) -> int:
    """
    Computes relative register of element of the array based on array declaration.
    Example: if array is like: a(-5,10) then a(-5) = 0, a(0) = 5 etc.
    """
    if user_typed_element_index < declaration.begin_index.value or \
            user_typed_element_index > declaration.end_index.value:
        raise IndexError(
                'An attempt to compute real register from user_register being out of range. Out of bounds error.')
    return user_typed_element_index - declaration.begin_index.value


def compute_real_register_of_array_element(
        declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]],
        identifier: ArrayElementByIntNumberIdentifier) -> int:
    """ Computes real register of element of the array based on declared array list."""
    return declared_arrays[identifier.array_identifier][0] + compute_relative_register_of_array_element(
        declared_arrays[identifier.array_identifier][2], identifier.index_value.value)


def generate_code_for_loading_array_element_by_variable(
        identifier: ArrayElementByVariableIdentifier,
        visitor: 'ASTInterpreter'
) -> str:
    """
    Generates code for loading value of array element which is indexed by variable. Load is called.
    Registers used: 0-5
    """
    return generate_code_for_computing_index_of_array_element_by_variable(identifier, visitor) + f'LOADI 0\n'


def generate_code_for_storing_array_element_by_variable(
        identifier: ArrayElementByVariableIdentifier,
        visitor: 'ASTInterpreter'
) -> str:
    """
    Generates code for storing value of array element which is indexed by variable. Store is called.
    Registers used: 0-5
    """
    return generate_code_for_computing_index_of_array_element_by_variable(identifier, visitor=visitor) + f'STOREI 0\n'


# and taken from known registers
def generate_code_for_computing_index_of_array_element_by_variable(
        identifier: ArrayElementByVariableIdentifier,
        visitor: 'ASTInterpreter'
) -> str:
    """
    Generates code for computing index of array element which is indexed by variable.
    Computed index (result) is present in register 0 (p0).
    Example: arr(b) is computed from b_value_reg - arr_fictional_indexing_start_register + arr_real_start_register
    Registers used: 0-5
    """
    if identifier.index_identifier not in visitor.declared_variables:
        raise UndeclaredVariableException(f"Variable '{identifier.index_identifier}' was not declared.",
                                          occurrence_place=identifier.start_position)
    if identifier.array_identifier not in visitor.declared_arrays:
        raise UndeclaredArrayException(f"Array '{identifier.array_identifier}' was not declared.",
                                       occurrence_place=identifier.start_position)

    arr_start = visitor.declared_variables[identifier.index_identifier]
    # return generate_number(
    #     visitor.declared_arrays[identifier.array_identifier][0], visitor.constants, destination_register=5) + \
    #     generate_number(
    #         visitor.declared_arrays[identifier.array_identifier][2].begin_index.value, visitor.constants,
    #         destination_register=4) + \
    #     f'LOAD {arr_start}\n' + f'SUB 4\n' + f'ADD 5\n'
    return generate_number(
        visitor.declared_arrays[identifier.array_identifier][0] -
        visitor.declared_arrays[identifier.array_identifier][2].begin_index.value,
        visitor.constants, destination_register=5) + \
        f'LOAD {arr_start}\n' + f'ADD 5\n'
