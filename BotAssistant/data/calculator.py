import ast
import operator
from aiogram.exceptions import TelegramBadRequest
class Calculator(ast.NodeVisitor):
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: self.sqrt,
            ast.USub: operator.neg
        }

    def sqrt(self, left, right):
        if left < 0 and right % 2 == 0:
            raise ValueError("Невозможно вычислить четный корень из отрицательного числа")
        return left ** (1 / right)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return self.operators[type(node.op)](left, right)

    def visit_Num(self, node):
        return node.n

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        return self.operators[type(node.op)](operand)

    def eval(self, expr):
        return self.visit(ast.parse(expr, mode='eval').body)

def calculate_expression(expression):
    calculator = Calculator()
    try:
        result = calculator.eval(expression)
        return result
    except Exception:
        return False
