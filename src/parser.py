from sly import Parser
from lexer import CompilerLexer


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    debugfile = 'parser.out'

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p):
        pass

    @_('BEGIN commands END')
    def program(self, p):
        pass

    @_('declarations "," IDENTIFIER')
    def declarations(self, p):
        pass

    @_('declarations "," IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p):
        pass

    @_('IDENTIFIER')
    def declarations(self, p):
        pass

    @_('IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p):
        pass

    @_('commands command')
    def commands(self, p):
        pass

    @_('command')
    def commands(self, p):
        pass

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        pass

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        pass

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        pass

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        pass

    @_('DO commands WHILE condition ENDDO')
    def command(self, p):
        pass

    @_('FOR IDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p):
        pass

    @_('FOR IDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p):
        pass

    @_('READ identifier ";"')
    def command(self, p):
        pass

    @_('WRITE value ";"')
    def command(self, p):
        pass

    @_('value')
    def expression(self, p):
        pass

    @_('value PLUS value')
    def expression(self, p):
        pass

    @_('value MINUS value')
    def expression(self, p):
        pass

    @_('value TIMES value')
    def expression(self, p):
        pass

    @_('value DIV value')
    def expression(self, p):
        pass

    @_('value MOD value')
    def expression(self, p):
        pass

    @_('value EQ value')
    def condition(self, p):
        pass

    @_('value NEQ value')
    def condition(self, p):
        pass

    @_('value LE value')
    def condition(self, p):
        pass

    @_('value GE value')
    def condition(self, p):
        pass

    @_('value LEQ value')
    def condition(self, p):
        pass

    @_('value GEQ value')
    def condition(self, p):
        pass

    @_('NUMBER')
    def value(self, p):
        pass

    @_('identifier')
    def value(self, p):
        pass

    @_('IDENTIFIER')
    def identifier(self, p):
        pass

    @_('IDENTIFIER "(" IDENTIFIER ")"')
    def identifier(self, p):
        pass

    @_('IDENTIFIER "(" NUMBER ")"')
    def identifier(self, p):
        pass


if __name__ == '__main__':
    lexer = CompilerLexer()
    parser = CompilerParser()

    with open('test1', 'r') as file:
        data = file.read()
        result = parser.parse(lexer.tokenize(data))
        print(result)

    # while True:
    #     try:
    #         text = input('calc > ')
    #         result = parser.parse(lexer.tokenize(text))
    #         print(result)
    #     except EOFError:
    #         break
