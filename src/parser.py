import sys

from sly import Parser
from label_converter.label_converter import convert_labels_to_registers
from lexer import CompilerLexer
from structures.ast.AST import *
from utils.AST_interpreter import ASTInterpreter
from utils.compilation_exceptions import CompilationException
from utils.test_utils import run_code


class CompilerParser(Parser):
    tokens = CompilerLexer.tokens
    # debugfile = 'parser.out'

    @_('DECLARE declarations BEGIN commands END')
    def program(self, p) -> Program:
        return Program(declarations=p.declarations, commands=p.commands)

    @_('BEGIN commands END')
    def program(self, p) -> Program:
        return Program(declarations=Declarations(list()), commands=p.commands)

    @_('declarations "," IDENTIFIER')
    def declarations(self, p) -> Declarations:
        p.declarations.add_declaration(NumberDeclaration(p.IDENTIFIER, start_position=(p.lineno, p.index)))
        return p.declarations

    @_('declarations "," IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p) -> Declarations:
        p.declarations.add_declaration(ArrayDeclaration(
            p.IDENTIFIER,
            begin_index=IntNumberValue(int(p.NUMBER0), start_position=(p.lineno, p.index)),
            end_index=IntNumberValue(int(p.NUMBER1), start_position=(p.lineno, p.index)),
            start_position=(p.lineno, p.index)))
        return p.declarations

    @_('IDENTIFIER')
    def declarations(self, p) -> Declarations:
        return Declarations(declarations=[NumberDeclaration(p.IDENTIFIER, start_position=(p.lineno, p.index))],
                            start_position=(p.lineno, p.index))

    @_('IDENTIFIER "(" NUMBER ":" NUMBER ")"')
    def declarations(self, p) -> Declarations:
        return Declarations(declarations=[ArrayDeclaration(
            p.IDENTIFIER,
            begin_index=IntNumberValue(int(p.NUMBER0), start_position=(p.lineno, p.index)),
            end_index=IntNumberValue(int(p.NUMBER1), start_position=(p.lineno, p.index)))],
                            start_position=(p.lineno, p.index))

    @_('commands command')
    def commands(self, p) -> Commands:
        p.commands.add_command(p.command)
        return p.commands

    @_('command')
    def commands(self, p) -> Commands:
        return Commands([p.command])

    @_('identifier ASSIGN expression ";"')
    def command(self, p) -> AssignmentCommand:
        return AssignmentCommand(p.identifier, p.expression, start_position=(p.lineno, p.index))

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p) -> IfThenElseCommand:
        return IfThenElseCommand(p.condition, p.commands0, p.commands1, start_position=(p.lineno, p.index))

    @_('IF condition THEN commands ENDIF')
    def command(self, p) -> IfThenCommand:
        return IfThenCommand(p.condition, p.commands, start_position=(p.lineno, p.index))

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p) -> WhileDoCommand:
        return WhileDoCommand(p.condition, p.commands, start_position=(p.lineno, p.index))

    @_('DO commands WHILE condition ENDDO')
    def command(self, p) -> DoWhileCommand:
        return DoWhileCommand(p.condition, p.commands, start_position=(p.lineno, p.index))

    @_('FOR IDENTIFIER FROM value TO value DO commands ENDFOR')
    def command(self, p) -> ForCommand:
        return ForCommand(iterator_identifier=p.IDENTIFIER, start=p.value0,
                          end=p.value1, is_down_to=False, commands=p.commands, start_position=(p.lineno, p.index))

    @_('FOR IDENTIFIER FROM value DOWNTO value DO commands ENDFOR')
    def command(self, p) -> ForCommand:
        return ForCommand(iterator_identifier=p.IDENTIFIER, start=p.value0,
                          end=p.value1, is_down_to=True, commands=p.commands, start_position=(p.lineno, p.index))

    @_('READ identifier ";"')
    def command(self, p) -> ReadCommand:
        return ReadCommand(p.identifier, start_position=(p.lineno, p.index))

    @_('WRITE value ";"')
    def command(self, p) -> WriteCommand:
        return WriteCommand(p.value, start_position=(p.lineno, p.index))

    @_('value')
    def expression(self, p) -> ExpressionHavingOneValue:
        return ExpressionHavingOneValue(p.value)

    @_('value PLUS value',
       'value MINUS value',
       'value TIMES value',
       'value DIV value',
       'value MOD value')
    def expression(self, p) -> ExpressionHavingTwoValues:
        return ExpressionHavingTwoValues(value1=p.value0, value2=p.value1, operation=p[1],
                                         start_position=(p.lineno, p.index))

    @_('value EQ value',
       'value NEQ value',
       'value LE value',
       'value GE value',
       'value LEQ value',
       'value GEQ value')
    def condition(self, p) -> TwoValueCondition:
        return TwoValueCondition(p.value0, p.value1, p[1], start_position=(p.lineno, p.index))

    @_('NUMBER')
    def value(self, p) -> IntNumberValue:
        return IntNumberValue(int(p.NUMBER), start_position=(p.lineno, p.index))

    @_('identifier')
    def value(self, p) -> IdentifierValue:
        return IdentifierValue(p.identifier)

    @_('IDENTIFIER')
    def identifier(self, p) -> VariableIdentifier:
        return VariableIdentifier(p.IDENTIFIER, start_position=(p.lineno, p.index))

    @_('IDENTIFIER "(" IDENTIFIER ")"')
    def identifier(self, p) -> ArrayElementByVariableIdentifier:
        return ArrayElementByVariableIdentifier(p.IDENTIFIER0, p.IDENTIFIER1, start_position=(p.lineno, p.index))

    @_('IDENTIFIER "(" NUMBER ")"')
    def identifier(self, p) -> ArrayElementByIntNumberIdentifier:
        return ArrayElementByIntNumberIdentifier(
            p.IDENTIFIER, IntNumberValue(int(p.NUMBER),
                                         start_position=(p.lineno, p.index)),
            start_position=(p.lineno, p.index))

    def error(self, token):
        if token:
            sys.stderr.write(f"Unrecognized symbol(s): '{token.value}'. Line number: {token.lineno} ({token.index}).\n"
                             f"ERROR for token: {token}.\n")
        else:
            sys.stderr.write("Parse error has occurred.\n")
        sys.exit(0)


if __name__ == '__main__':
    lexer = CompilerLexer()
    parser = CompilerParser()

    if len(sys.argv) >= 3:
        src_file = sys.argv[1]
        out_file = sys.argv[2]
    else:
        print("Correct arguments for the program are: <source filename> <executable filename>.")
        sys.exit(0)

    with open(src_file, 'r') as file:
        data = file.read()
        # print(list(lexer.tokenize(data)))
        tokens = lexer.tokenize(data)
        # pprint(list(tokens))
        result: Program = parser.parse(tokens)
        # print(result)
        try:
            print(f"Compiling file {src_file}.")
            interpreter = ASTInterpreter(result)
            code: str = result.accept(visitor=interpreter)
            print("File compiled successfully to intermediate representation.")
            print(f"Replacing labels and generating executable code to {out_file}.")

            if len(sys.argv) >= 3 and sys.argv[2] == '--run':
                print('RUNNING CODE')
                out = run_code(code, f'exe_{src_file}', *sys.argv[3:],
                               path_to_vm='../maszyna_wirtualna/maszyna-wirtualna-cln')
                print(out)
            else:
                convert_labels_to_registers(code, output_filename=out_file)

            print(f"Compilation finished successfully.")

        except CompilationException as e:
            print(f'A compilation error has occurred in line {e.occurrence_place[0]}. {e}')


