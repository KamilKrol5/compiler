from utils.AST_interpreter import *
from utils.value_utils import generate_code_for_loading_value


class AnAttemptToModifyCounterException(Exception):
    pass


''' Writes code for if then command in visitor.
    All its sub-commands are generated too.'''


def write_code_for_if_then_command(
        command: IfThenCommand,
        visitor: 'ASTInterpreter'
) -> None:
    command.condition.accept(visitor)
    assembly_operation = {'LEQ': 'JPOS', 'GEQ': 'JNEG', 'LE': 'JNEG', 'GE': 'JPOS'}  # additional helping dictionary
    compare_operation: str = command.condition.compare_operation
    if isinstance(command.condition, TwoValueCondition):
        if compare_operation == 'NEQ':
            label = visitor.label_provider.get_label()
            visitor.generated_code.append(f'JZERO {label}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label}\n')
        elif compare_operation == 'EQ':
            label1 = visitor.label_provider.get_label()
            label2 = visitor.label_provider.get_label()
            visitor.generated_code.append(f'JZERO {label1}\n' + f'JUMP {label2}\n' + f'{label1}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label2}\n')
        # strict inequality
        elif compare_operation == 'LE' or compare_operation == 'GE':
            label_1 = visitor.label_provider.get_label()
            label_2 = visitor.label_provider.get_label()
            visitor.generated_code.append(f'{assembly_operation[compare_operation]} {label_1}\n' + \
                                          f'JUMP {label_2}\n' + \
                                          f'{label_1}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label_2}\n')
        # not strict inequality
        elif compare_operation == 'LEQ' or compare_operation == 'GEQ':
            label = visitor.label_provider.get_label()
            visitor.generated_code.append(f'{assembly_operation[compare_operation]} {label}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label}\n')
        # unknown compare operator
        else:
            raise ValueError('Unknown compare_operation has occurred.')

    else:
        raise \
            ValueError('Unknown instance of Condition has occurred. Only TwoValueCondition is supported in this method')


''' Writes code for if then else command in visitor.
    All its sub-commands are generated too.'''


def write_code_for_if_then_else_command(
        command: IfThenElseCommand,
        visitor: 'ASTInterpreter'
) -> None:
    command.condition.accept(visitor)
    assembly_operation = {'LEQ': 'JPOS', 'GEQ': 'JNEG', 'LE': 'JNEG', 'GE': 'JPOS'}  # additional helping dictionary
    compare_operation: str = command.condition.compare_operation
    if isinstance(command.condition, TwoValueCondition):
        if compare_operation == 'NEQ':
            label_false = visitor.label_provider.get_label()
            label_end = visitor.label_provider.get_label()
            visitor.generated_code.append(f'JZERO {label_false}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'JUMP {label_end}\n' \
                                          + f'{label_false}\n')
            for c in command.commands_false.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label_end}\n')
        elif compare_operation == 'EQ':
            label1 = visitor.label_provider.get_label()
            label2 = visitor.label_provider.get_label()
            visitor.generated_code.append(f'JZERO {label1}\n')
            for c in command.commands_false.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'JUMP {label2}\n' + f'{label1}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label2}\n')
        # strict inequality
        elif compare_operation == 'LE' or compare_operation == 'GE':
            label_1 = visitor.label_provider.get_label()
            label_2 = visitor.label_provider.get_label()
            visitor.generated_code.append(f'{assembly_operation[compare_operation]} {label_1}\n')
            for c in command.commands_false.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'JUMP {label_2}\n' + \
                                          f'{label_1}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label_2}\n')
        # not strict inequality
        elif compare_operation == 'LEQ' or compare_operation == 'GEQ':
            label = visitor.label_provider.get_label()
            label_end = visitor.label_provider.get_label()
            visitor.generated_code.append(f'{assembly_operation[compare_operation]} {label}\n')
            for c in command.commands_true.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'JUMP {label_end}\n' + \
                                          f'{label}\n')
            for c in command.commands_false.commands:
                c.accept(visitor)
            visitor.generated_code.append(f'{label_end}\n')
        # unknown compare operator
        else:
            raise ValueError('Unknown compare_operation has occurred.')

    else:
        raise \
            ValueError('Unknown instance of Condition has occurred. Only TwoValueCondition is supported in this method')


''' Writes code for an assignment command in visitor.
    Value of expression (which is assignment's field) is stored in register related to
    given identifier (which is also assignment's field).'''


def write_code_for_assignment_command(
        command: AssignmentCommand,
        visitor: 'ASTInterpreter'
) -> None:
    if visitor.is_identifier_local_variable(command.identifier):
        raise AnAttemptToModifyCounterException(
            f"An attempt to modify iterator '{command.identifier}'' inside a for loop. Iterator cannot be modified.")
    register: AbstractIdentifierAccess = command.identifier.accept(visitor)
    visitor.generated_code.append(register.prepare_register())
    command.expression.accept(visitor)
    visitor.generated_code.append(register.store())


''' Writes code for while do loop to visitor's generated code.'''


def write_code_for_while_do_command(
        command: WhileDoCommand,
        visitor: 'ASTInterpreter'
) -> None:
    label_start = visitor.label_provider.get_label()
    label_end = visitor.label_provider.get_label()

    if command.is_user_command:
        visitor.generated_code.append(f'## BEGIN while-do loop\n')

    visitor.generated_code.append(f'{label_start}\n')
    if_help = IfThenElseCommand(
        condition=command.condition,
        commands_true=Commands(command.commands.commands + [JumpCommand(label_start)]),
        commands_false=Commands([
            JumpCommand(label_end)
        ]))
    if_help.accept(visitor)
    visitor.generated_code.append(f'{label_end}\n')
    if command.is_user_command:
        visitor.generated_code.append(f'## END while-do loop\n')


def write_code_for_do_while_command(
        command: DoWhileCommand,
        visitor: 'ASTInterpreter'
) -> None:
    label_start = visitor.label_provider.get_label()
    visitor.generated_code.append(f'## BEGIN do-while loop\n{label_start}\n')
    if_help = IfThenCommand(
        condition=command.condition,
        commands=Commands([JumpCommand(label_start)]))
    command.commands.accept(visitor)
    if_help.accept(visitor)
    visitor.generated_code.append(f'## END do-while loop\n')


def write_code_for_for_loop_command(
        loop: ForCommand,
        visitor: 'ASTInterpreter'
) -> None:
    loop_name: str = visitor.loop_name_provider.get_label()
    iterator_variable: str = loop.iterator_identifier
    end_variable: str = f'{loop_name}_@end'

    # counter_var: str = f'{loop_name}_@counter'  # stores an amount of iterations to be performed

    # iterator and counter_var declaration (as a local variables)
    # check if iterator name can be declared will be performed, error if there is a variable with the same name declared
    visitor.add_local_variable(iterator_variable)
    visitor.add_local_variable(end_variable)

    end_reg = visitor.local_variables[end_variable]
    iterator_reg = visitor.local_variables[iterator_variable]

    # generate caption
    to_or_downto = 'DOWN TO' if loop.is_down_to else 'TO'
    start_str = loop.start.value if isinstance(loop.start, IntNumberValue) else '?'
    end_str = loop.end.value if isinstance(loop.end, IntNumberValue) else '?'
    code: str = f'## BEGIN for loop: {loop_name} FROM {loop.iterator_identifier} := {start_str} {to_or_downto}' \
                    f' {end_str}\n'
    # load loop.start value into iterator_reg
    code = code + generate_code_for_loading_value(loop.start, visitor)
    code = code + f'STORE {iterator_reg} # {iterator_variable}\n'  # loop.start load into iteration_register

    # # load abs(loop.end - loop.start) + 1 into counter_reg
    # code = code + generate_code_for_expression(ExpressionHavingTwoValues(loop.end, loop.start, 'MINUS'), visitor)
    # code = code + generate_abs(visitor.label_provider) + f'INC\nSTORE {counter_reg}\n'

    code = code + generate_code_for_loading_value(loop.end, visitor) + \
        f'STORE {end_reg} # {end_variable}\n'
    visitor.generated_code.append(code)
    # now iterator and end variables are computed and are resistant to start/end variables modification inside the loop

    comparison_signs = {False: 'LEQ', True: 'GEQ'}

    while_do = WhileDoCommand(
        TwoValueCondition(
            IdentifierValue(VariableIdentifier(iterator_variable)),
            IdentifierValue(VariableIdentifier(end_variable)),
            comparison_signs[loop.is_down_to]),
        Commands(loop.commands.commands + [IncrementDecrementCommand(
            VariableIdentifier(iterator_variable),
            is_decrement=loop.is_down_to)]),
        is_user_command=False)

    while_do.accept(visitor)
    code = f'## END loop: {loop_name}\n'
    visitor.generated_code.append(code)

    # iterator and counter_var local variables removal
    visitor.remove_local_variable(iterator_variable)
    visitor.remove_local_variable(end_variable)
