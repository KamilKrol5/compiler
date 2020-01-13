from utils.AST_interpreter import *
from utils.arrays_utils import generate_code_for_loading_array_element_by_variable, \
    compute_real_register_of_array_element
from utils.math_utils import generate_number

''' Generates code for loading numeric value of Value object to the register 0 (p0).
    Each subclass of Value is supported.'''


def generate_code_for_loading_value(
        value: Value,
        visitor: 'ASTInterpreter'
) -> str:
    if isinstance(value, IntNumberValue):
        return generate_number(value.value, constants=visitor.constants)
    elif isinstance(value, IdentifierValue):
        if isinstance(value.identifier, VariableIdentifier):
            if value.identifier.identifier_name in visitor.declared_variables.keys():
                return f'LOAD {visitor.declared_variables[value.identifier.identifier_name]}\n'
            elif value.identifier.identifier_name in visitor.local_variables.keys():
                return f'LOAD {visitor.local_variables[value.identifier.identifier_name]}\n'
            else:
                ValueError('Neither declared_variables nor local_variables dictionary '
                           'does not contain key - identifier name provided with '
                           'write_command`s property - identifier. '
                           f'Variable {value.identifier.identifier_name} might not be declared.')
        elif isinstance(value.identifier, ArrayElementByIntNumberIdentifier):
            if value.identifier.array_identifier not in visitor.declared_arrays.keys():
                ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            return f'LOAD {compute_real_register_of_array_element(visitor.declared_arrays, value.identifier)}\n'
        elif isinstance(value.identifier, ArrayElementByVariableIdentifier):
            if value.identifier.array_identifier not in visitor.declared_arrays.keys():
                ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                           'write_command`s property - identifier. Variable might not be declared.')
            loading_array_element: str = generate_code_for_loading_array_element_by_variable(
                value.identifier, visitor)
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
        visitor: 'ASTInterpreter'
) -> int:
    if isinstance(value.identifier, VariableIdentifier):
        if value.identifier.identifier_name in visitor.declared_variables.keys():
            return visitor.declared_variables[value.identifier.identifier_name]
        elif value.identifier.identifier_name in visitor.local_variables.keys():
            return visitor.local_variables[value.identifier.identifier_name]
        else:
            ValueError('Neither declared_variables nor local_variables dictionary '
                       'does not contain key - identifier name provided with '
                       f'write_command`s property - identifier. '
                       f'Variable {value.identifier.identifier_name} might not be declared.')
    elif isinstance(value.identifier, ArrayElementByIntNumberIdentifier):
        if value.identifier.array_identifier not in visitor.declared_arrays.keys():
            ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                       'write_command`s property - identifier. Variable might not be declared.')
        return compute_real_register_of_array_element(visitor.declared_arrays, value.identifier)
    elif isinstance(value.identifier, ArrayElementByVariableIdentifier):
        raise ValueError('Cannot compute register of value which identifier is ArrayElementByVariableIdentifier.'
                         'Separate assembly code needs to be created to do so.')
    else:
        raise ValueError('Unknown instance of Identifier occurred.')


''' Loads variable defined in identifier to dest_register (default is 0).
    If variable name is not present in the declared_variables dictionary an exception is raised
    Registers used: 0-5'''


def load_value_by_identifier(identifier: Identifier, visitor: 'ASTInterpreter', dest_register=0) -> str:
    result: str = f'## load value by identifier begin\n'
    if isinstance(identifier, VariableIdentifier):
        if identifier.identifier_name in visitor.declared_variables.keys():
            register_to_load = visitor.declared_variables[identifier.identifier_name]
        elif identifier.identifier_name in visitor.local_variables.keys():
            register_to_load = visitor.local_variables[identifier.identifier_name]
        else:
            raise ValueError(f'Neither declared_variables nor local_variables dictionary'
                             ' does not contain key - identifier name provided with '
                             f'"identifier" argument. Variable {identifier.identifier_name} might not be declared.')
        result = result + f'LOAD {register_to_load}\n'
    elif isinstance(identifier, ArrayElementByIntNumberIdentifier):
        if identifier.array_identifier not in visitor.declared_arrays.keys():
            raise ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        result = result + f'LOAD {compute_real_register_of_array_element(visitor.declared_arrays, identifier)}\n'
    elif isinstance(identifier, ArrayElementByVariableIdentifier):
        if identifier.array_identifier not in visitor.declared_arrays.keys():
            raise ValueError('declared_arrays dictionary does not contain key - identifier name provided with '
                             '"identifier" argument. Variable might not be declared.')
        if identifier.index_identifier not in visitor.declared_variables.keys() and\
                identifier.index_identifier not in visitor.local_variables.keys():
            raise ValueError(f'Neither declared_variables nor local_variables dictionary'
                             ' does not contain key - identifier name provided with '
                             f'"identifier" argument. Variable {identifier.index_identifier} might not be declared.')

        result = result + generate_code_for_loading_array_element_by_variable(identifier, visitor)

    if dest_register != 0:
        result = result + f'STORE {dest_register}\n'
    return result + f'## load value by identifier end\n'
