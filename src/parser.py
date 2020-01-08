from sly import Parser
from lexer import CompilerLexer
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    debugfile = 'parser.out'

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p) -> Program:
        return Program(declarations=p.declarations, commands=p.commands)

    @_('BEGIN commands END')
    def program(self, p) -> Program:
        return Program(declarations=Declarations(List()), commands=p.commands)

    @_('declarations "," IDENTIFIER')
    def declarations(self, p) -> Declarations:
        p.declarations.add_declaration(NumberDeclaration(p.IDENTIFIER))
        return p.declarations

    @_('declarations "," IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p) -> Declarations:
        p.declarations.add_declaration(ArrayDeclaration(p.IDENTIFIER, begin_index=IntNumberValue(int(p.NUMBER0)),
                                                        end_index=IntNumberValue(int(p.NUMBER1))))
        return p.declarations

    @_('IDENTIFIER')
    def declarations(self, p) -> Declarations:
        return Declarations(declarations=[NumberDeclaration(p.IDENTIFIER)])

    @_('IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p) -> Declarations:
        return Declarations(declarations=[ArrayDeclaration(p.IDENTIFIER, begin_index=IntNumberValue(int(p.NUMBER0)),
                                                           end_index=IntNumberValue(int(p.NUMBER1)))])

    @_('commands command')
    def commands(self, p) -> Commands:
        p.commands.add_command(p.command)
        return p.commands

    @_('command')
    def commands(self, p) -> Commands:
        return Commands([p.command])

    @_('identifier ASSIGN expression ";"')
    def command(self, p) -> AssignmentCommand:
        return AssignmentCommand(p.identifier, p.expression)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p) -> IfThenElseCommand:
        return IfThenElseCommand(p.condition, p.commands0, p.commands1)

    @_('IF condition THEN commands ENDIF')
    def command(self, p) -> IfThenCommand:
        return IfThenCommand(p.condition, p.commands)

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p) -> WhileDoCommand:
        return WhileDoCommand(p.condition, p.commands)

    @_('DO commands WHILE condition ENDDO')
    def command(self, p) -> DoWhileCommand:
        return DoWhileCommand(p.condition, p.commands)

    @_('FOR IDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p) -> ForCommand:
        return ForCommand(iterator_identifier=p.IDENTIFIER, start=p.value0,
                          end=p.value1, is_down_to=False, commands=p.commands)

    @_('FOR IDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p) -> ForCommand:
        return ForCommand(iterator_identifier=p.IDENTIFIER, start=p.value0,
                          end=p.value1, is_down_to=True, commands=p.commands)

    @_('READ identifier ";"')
    def command(self, p) -> ReadCommand:
        return ReadCommand(p.identifier)

    @_('WRITE value ";"')
    def command(self, p) -> WriteCommand:
        return WriteCommand(p.value)

    @_('value')
    def expression(self, p) -> ExpressionHavingOneValue:
        return ExpressionHavingOneValue(p.value)

    @_('value PLUS value',
       'value MINUS value',
       'value TIMES value',
       'value DIV value',
       'value MOD value')
    def expression(self, p) -> ExpressionHavingTwoValues:
        return ExpressionHavingTwoValues(value1=p.value0, value2=p.value1, operation=p[1])

    @_('value EQ value',
       'value NEQ value',
       'value LE value',
       'value GE value',
       'value LEQ value',
       'value GEQ value')
    def condition(self, p) -> TwoValueCondition:
        return TwoValueCondition(p.value0, p.value1, p[1])

    @_('NUMBER')
    def value(self, p) -> IntNumberValue:
        return IntNumberValue(int(p.NUMBER))

    @_('identifier')
    def value(self, p) -> IdentifierValue:
        return IdentifierValue(p.identifier)

    @_('IDENTIFIER')
    def identifier(self, p) -> VariableIdentifier:
        return VariableIdentifier(p.IDENTIFIER)

    @_('IDENTIFIER "(" IDENTIFIER ")"')
    def identifier(self, p) -> ArrayElementByVariableIdentifier:
        return ArrayElementByVariableIdentifier(p.IDENTIFIER0, p.IDENTIFIER1)

    @_('IDENTIFIER "(" NUMBER ")"')
    def identifier(self, p) -> ArrayElementByIntNumberIdentifier:
        return ArrayElementByIntNumberIdentifier(p.IDENTIFIER, IntNumberValue(int(p.NUMBER)))


if __name__ == '__main__':
    lexer = CompilerLexer()
    parser = CompilerParser()

    # with open('test2', 'r') as file:
    #     data = file.read()
    #     result = parser.parse(lexer.tokenize(data))
    #     print(result)

    with open('test2', 'r') as file:
        data = file.read()
        result = parser.parse(lexer.tokenize(data))
        print(result)
        interpreter = ASTInterpreter(result)

    # while True:
    #     try:
    #         text = input('calc > ')
    #         result = parser.parse(lexer.tokenize(text))
    #         print(result)
    #     except EOFError:
    #         break
