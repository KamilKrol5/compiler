from structures.ast.AST import Expression, ArrayDeclaration
from utils.math_operations_code_generator import MathOperationsCodeGenerator, Dict, Tuple
from utils.value_utils import generate_code_for_loading_value


''' Generates code for computing value of an expression.
    The value of expression is returned in register 0 (p0).
    Registers used: 0-7'''


def generate_code_for_expression(
        expression: Expression,
        declared_variables: Dict[str, int],
        declared_arrays: Dict[str, Tuple[int, int, ArrayDeclaration]]
) -> str:
    math_code_generator = MathOperationsCodeGenerator(declared_variables, declared_arrays)
    if expression.number_of_values() == 1:
        return generate_code_for_loading_value(expression.value, declared_variables, declared_arrays)
    elif expression.number_of_values() == 2:
        if expression.operation not in math_code_generator.expressions.keys():
            raise ValueError('Unknown operator. It is not present in expressions dictionary in expression_utils.')
        result: str = math_code_generator.expressions.get(expression.operation)(math_code_generator, expression)
        return result
    else:
        raise ValueError('Unknown instance of Expression occurred.\n'
                         'Provided expression is neither OneValueExpression nor TwoValueExpression')
