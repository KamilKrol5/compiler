from sly import Lexer


class CompilerLexer(Lexer):
    tokens = {PLUS, MINUS, TIMES, DIV, MOD,
              EQ, NEQ, LE, GE, LEQ, GEQ,
              ASSIGN,
              FOR, FROM, TO, DOWNTO,
              READ, WRITE,
              IF, THEN, ELSE, ENDIF,
              IDENTIFIER, NUMBER,
              DECLARE, BEGIN, END}

    literals = {'(', ')', ';', ',', ':'}

    ignore = r' \t'
    ignore_comment = r'\[[^\]]*\]'

    IDENTIFIER = r'[_a-z]+'
    PLUS = r'PLUS'
    MINUS = r'MINUS'
    TIMES = r'TIMES'
    DIV = r'DIV'
    MOD = r'MOD'
    EQ = r'EQ'
    NEQ = r'NEQ'
    LE = r'LE'
    GE = r'GE'
    LEQ = r'LEQ'
    GEQ = r'GEQ'
    ASSIGN = r'ASSIGN'
    FOR = r'FOR'
    FROM = r'FROM'
    TO = r'TO'
    DOWNTO = r'DOWNTO'
    READ = r'READ'
    WRITE = r'WRITE'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    ENDIF = r'ENDIF'
    DECLARE = r'DECLARE'
    BEGIN = r'BEGIN'
    END = r'END'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'Illegal character {t.value[0]}')
        self.index += 1


if __name__ == '__main__':
    data = '''
[ Counting 
lkkjkhk]
x ASSIGN 0; GG
FOR 1 TO 10
    WRITE x;
    x ASSIGN x PLUS 1;

'''
    lexer = CompilerLexer()
    for tok in lexer.tokenize(data):
        print(tok)
