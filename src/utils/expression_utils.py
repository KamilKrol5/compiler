from utils.math_operations_code_generator import MathOperationsCodeGenerator, Expression
from utils.value_utils import generate_code_for_loading_value

''' Generates code for computing value of an expression.
    The value of expression is returned in register 0 (p0).
    Registers used: 0-7'''


# TODO move it
def generate_code_for_expression(
        expression: Expression,
        visitor: 'ASTInterpreter'
) -> str:
    math_code_generator = MathOperationsCodeGenerator(visitor)
    if expression.number_of_values() == 1:
        return generate_code_for_loading_value(expression.value, visitor)
    elif expression.number_of_values() == 2:
        if expression.operation not in math_code_generator.expressions.keys():
            raise ValueError('Unknown operator. It is not present in expressions dictionary in expression_utils.')
        result: str = math_code_generator.expressions.get(expression.operation)(math_code_generator, expression)
        return result
    else:
        raise ValueError('Unknown instance of Expression occurred.\n'
                         'Provided expression is neither OneValueExpression nor TwoValueExpression')
