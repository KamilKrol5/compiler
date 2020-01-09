from utils.AST_interpreter import *

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
    visitor.generated_code.append(f'## BEGIN while do loop\n{label_start}\n')
    if_help = IfThenElseCommand(
        condition=command.condition,
        commands_true=Commands(command.commands.commands + [JumpCommand(label_start)]),
        commands_false=Commands([
            JumpCommand(label_end)
        ]))
    if_help.accept(visitor)
    visitor.generated_code.append(f'{label_end}\n## END while do loop\n')
