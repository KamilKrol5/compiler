from utils.AST_interpreter import *


def generate_code_for_if_then_command(
        command: IfThenCommand,
        visitor: 'ASTInterpreter'
) -> str:
    result: str = command.condition.accept(visitor)
    assembly_operation = {'LEQ': 'JPOS', 'GEQ': 'JNEG', 'LE': 'JNEG', 'GE': 'JPOS'}  # additional helping dictionary
    compare_operation: str = command.condition.compare_operation
    if isinstance(command.condition, TwoValueCondition):
        if compare_operation == 'NEQ':
            label = visitor.label_provider.get_label()
            result = result + f'JZERO {label}\n'
            for c in command.commands_true.commands:
                result = result + c.accept(visitor)
            result = result + f'{label}\n'
        elif compare_operation == 'EQ':
            label1 = visitor.label_provider.get_label()
            label2 = visitor.label_provider.get_label()
            result = result + f'JZERO {label1}\n' + f'JUMP {label2}\n' + f'{label1}\n'
            for c in command.commands_true.commands:
                result = result + c.accept(visitor)
            result = result + f'{label2}\n'
        # strict inequality
        elif compare_operation == 'LE' or compare_operation == 'GE':
            label_1 = visitor.label_provider.get_label()
            label_2 = visitor.label_provider.get_label()
            result = result + f'{assembly_operation[compare_operation]} {label_1}\n' +\
                f'JUMP {label_2}\n' +\
                f'{label_1}\n'
            for c in command.commands_true.commands:
                result = result + c.accept(visitor)
            result = result + f'{label_2}\n'
        # not strict inequality
        elif compare_operation == 'LEQ' or compare_operation == 'GEQ':
            label = visitor.label_provider.get_label()
            result = result + f'{assembly_operation[compare_operation]} {label}\n'
            for c in command.commands_true.commands:
                result = result + c.accept(visitor)
            result = result + f'{label}\n'
        # unknown compare operator
        else:
            raise ValueError('Unknown compare_operation has occurred.')

    else:
        raise \
            ValueError('Unknown instance of Condition has occurred. Only TwoValueCondition is supported in this method')
    return result
