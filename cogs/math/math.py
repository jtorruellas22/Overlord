from discord.ext import commands

import ast
import math
import operator
import re

OPERATIONS = {
    # operations represented by symbols
    ast.Add: operator.add, # addition
    ast.BitXor: operator.pow, # exponentiation
    ast.Div: operator.truediv, # division
    ast.Mult: operator.mul, # multiplication
    ast.Mod: operator.mod, # modulo
    ast.Sub: operator.sub, # subtraction

    # operations represented by names
    "abs": lambda args: abs(args[0]), # absolute value
    "cos": lambda args: math.cos(args[0]), # cosine
    "sin": lambda args: math.sin(args[0]), # sine
    "sqrt": lambda args: math.sqrt(args[0]), # square root
    "tan": lambda args: math.tan(args[0]) # tangent
}

CONSTANTS = {
    "e": math.e,
    "pi": math.pi
}

def evaluate_node(node):
    # numbers
    if isinstance(node, ast.Num):
        return node.n

    # constants
    elif isinstance(node, ast.Name):
        const_name = node.id

        if const_name in CONSTANTS:
            return CONSTANTS[const_name]
        else:
            raise Exception(f"no such constant '{const_name}' supported")

    # unary operators
    elif isinstance(node, ast.UnaryOp):
        op = OPERATIONS[type(node.op)]

        # evaluate the argument first
        arg = evaluate_node(node.operand)

        return op(arg)

    # binary operators
    elif isinstance(node, ast.BinOp):
        op = OPERATIONS[type(node.op)]

        # evaluate both arguments first
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return op(left, right)

    # named functions
    elif isinstance(node, ast.Call):
        op = OPERATIONS[node.func.id]

        # evaluate the arguments first
        args = [evaluate_node(arg) for arg in node.args]

        return op(args)

    # unknown or unsupported
    else:
        raise TypeError("unknown or unsupported operator/function")

def evaluate(expression):
    return evaluate_node(ast.parse(expression, mode="eval").body)

def handle_implicit_mul(expression):
    # product of two expressions enclosed by parentheses
    expression = expression.replace(")(", ")*(")

    # digit followed by letter or opening parentheses
    expression = re.sub(r"([0-9])([A-Za-z\(])", r"\1*\2", expression)

    # closing parentheses followed by digit/letter
    expression = re.sub(r"\)([0-9A-Za-z])", r")*\1", expression)

    return expression

class BasicMath(commands.Cog, name="Basic Math"):
    """Calculates basic math"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def calc(self, context, *, expression):
        """Evaluate the given mathematical expression."""

        try:
            await context.reply(evaluate(handle_implicit_mul(expression)))
        except Exception as e:
            await context.reply(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BasicMath(bot))
