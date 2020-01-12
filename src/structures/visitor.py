from structures.ast.AST import *


class Visitor(ABC):

    def visit_int_number_value(self, int_number_value: 'IntNumberValue'):
        pass

    def visit_identifier_value(self, identifier_value: 'IdentifierValue'):
        identifier_value.identifier.accept(self)

    def visit_array_element_by_variable_identifier(
            self, array_element_by_variable_identifier: 'ArrayElementByVariableIdentifier'):
        pass

    def visit_array_element_by_int_number_identifier(
            self, array_element_by_int_number_identifier: 'ArrayElementByIntNumberIdentifier'):
        array_element_by_int_number_identifier.index_value.accept(self)

    def visit_variable_identifier(self, variable_identifier: 'VariableIdentifier'):
        pass

    def visit_number_declaration(self, number_declaration: 'NumberDeclaration'):
        pass

    def visit_array_declaration(self, array_declaration: 'ArrayDeclaration'):
        array_declaration.begin_index.accept(self)
        array_declaration.end_index.accept(self)

    def visit_declarations(self, declarations: 'Declarations'):
        for d in declarations.declarations:
            d.accept(self)

    def visit_expression_having_one_value(self, expression: 'ExpressionHavingOneValue'):
        expression.value.accept(self)

    def visit_expression_having_two_values(self, expression: 'ExpressionHavingTwoValues'):
        expression.valueLeft.accept(self)
        expression.valueRight.accept(self)

    def visit_two_value_condition(self, condition: 'TwoValueCondition'):
        condition.valueLeft.accept(self)
        condition.valueRight.accept(self)

    def visit_commands(self, commands: 'Commands'):
        for c in commands.commands:
            c.accept(self)

    def visit_assignment_command(self, assignment_command: 'AssignmentCommand'):
        assignment_command.identifier.accept(self)
        assignment_command.expression.accept(self)

    def visit_if_then_else_command(self, if_then_else_command: 'IfThenElseCommand'):
        if_then_else_command.condition.accept(self)
        if_then_else_command.commands_true.accept(self)
        if_then_else_command.commands_false.accept(self)

    def visit_if_then_command(self, if_then_command: 'IfThenCommand'):
        if_then_command.condition.accept(self)
        if_then_command.commands_true.accept(self)

    def visit_while_do_command(self, while_do_command: 'WhileDoCommand'):
        while_do_command.condition.accept(self)
        while_do_command.commands.accept(self)

    def visit_do_while_command(self, do_while_command: 'DoWhileCommand'):
        do_while_command.condition.accept(self)
        do_while_command.commands.accept(self)

    def visit_for_command(self, for_command: 'ForCommand'):
        for_command.start.accept(self)
        for_command.end.accept(self)
        for_command.commands.accept(self)

    def visit_read_command(self, read_command: 'ReadCommand'):
        read_command.identifier.accept(self)

    def visit_write_command(self, write_command: 'WriteCommand'):
        write_command.value.accept(self)

    def visit_program(self, program: 'Program'):
        program.declarations.accept(self)
        program.commands.accept(self)

    def visit_jump_command(self, jump_command: 'JumpCommand'):
        pass

    def visit_increment_decrement_command(self, increment_decrement_command: 'IncrementDecrementCommand'):
        increment_decrement_command.identifier.accept(self)
