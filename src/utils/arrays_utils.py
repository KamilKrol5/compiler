from structures.AST import *
from typing import Dict, Tuple

''' Computes relative register of element of the array based on array declaration.
    Example: if array is like: a(-5,10) then a(-5) = 0, a(0) = 5 etc.'''


def compute_relative_register_of_array_element(declaration: ArrayDeclaration, user_typed_element_index: int) -> int:
    if user_typed_element_index < declaration.begin_index.value or user_typed_element_index > declaration.end_index.value:
        raise \
            IndexError(
                'An attempt to compute real register from user_register being out of range. Out of bounds error.')
    return user_typed_element_index - declaration.begin_index.value


''' Computes real register of element of the array based on declared array list.'''


def compute_real_register_of_array_element(declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]],
                                           identifier: str, user_typed_element_index: int) -> int:
    return declared_arrays[identifier][0] + compute_relative_register_of_array_element(declared_arrays[identifier][2],
                                                                                       user_typed_element_index)
