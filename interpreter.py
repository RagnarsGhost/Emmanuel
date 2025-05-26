from Token import Types
from data import Data
from ast_nodes import BinOp, UnaryOp, Number, Boolean, String, Var, Print, Assign

class My_RuntimeError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"MyRuntimeError: {self.message}"

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.global_env = {}

    def interpret(self):
        statements = self.parser.parse()
        return self.visit_list(statements)



    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        try:
            return visitor(node)
        except Exception as e:
            raise My_RuntimeError(f"Error visiting {type(node).__name__}: {e}")

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_Assign(self, node):
        value = self.visit(node.expr)
        self.global_env[node.name] = value
        return value

    def visit_Var(self, node):
        name = node.name
        if name in self.global_env:
            return self.global_env[name]
        raise My_RuntimeError(f"Undefined variable '{name}'")

    def visit_Print(self, node):
        value = self.visit(node.expr)
        print(value)
        # return value  # Optional

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == Types.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) and isinstance(right, (int, float)):
                return left + str(right)
            if isinstance(left, (int, float)) and isinstance(right, str):
                try:
                    right_str = str(right)
                    if '.' in right_str:
                        coerced = float(right_str)
                    else:
                        coerced = int(right_str)
                    return left + coerced
                except ValueError:
                    raise Exception("Cannot coerce left operand to number for + operation")
            else:
                raise Exception("Invalid operands for + operation")

        elif node.op.type == Types.MINUS:
            return left - right
        elif node.op.type == Types.MULTIPLY:
            return left * right
        elif node.op.type == Types.DIVIDE:
            return left / right
        elif node.op.type == Types.LTHAN:
            return left < right
        elif node.op.type == Types.GTHAN:
            return left > right
        elif node.op.type == Types.LTHANE:
            return left <= right
        elif node.op.type == Types.GTHANE:
            return left >= right
        elif node.op.type == Types.EQ:
            return left == right
        elif node.op.type == Types.NOTEQ:
            return left != right
        elif node.op.type == Types.AND:
            return left and right
        elif node.op.type == Types.OR:
            return left or right
        else:
            raise Exception("Unknown binary operator")

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        if node.op.type == Types.PLUS:
            return +expr
        elif node.op.type == Types.MINUS:
            return -expr
        elif node.op.type == Types.NOT:
            return not expr
        else:
            raise Exception("Unknown unary operator")

    def visit_Number(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Call(self, node):
        # Assuming node.func_name is a string representing the function name
        if node.func_name == "len":
            if len(node.args) != 1:
                raise Exception("len() takes exactly one argument")
            arg = self.visit(node.args[0])
            if not isinstance(arg, (str, list)):
                raise Exception("len() argument must be a string or list")
            return len(arg)
        raise Exception(f"Unknown function: {node.func_name}")

    def visit_list(self, node_list):
        result = None
        for node in node_list:
            result = self.visit(node)
        return result
