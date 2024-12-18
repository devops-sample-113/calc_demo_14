# calculate.py
import math

class Calculator:
    def __init__(self):
        self.operations = {
            "add": self.add,
            "sub": self.subtract,
            "mul": self.multiply,
            "div": self.divide,
            "pow": self.power
        }

    def calculate(self, operand1, operand2, operator):
        if operator in self.operations:
            try:
                result = self.operations[operator](operand1, operand2)
                return self.format_number(result)
            except ValueError as e:
                return str(e)
        else:
            return "Invalid operator"

    @staticmethod
    def format_number(value):
        if isinstance(value, (int, float)):
            if abs(value) < 1e-10:  # Handle very small numbers
                return 0
            if value.is_integer():
                return int(value)
            return round(value, 10)  # Limit decimal places
        return value

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if abs(y) < 1e-10:  # Better check for zero division
            raise ValueError("Error: Cannot divide by zero!")
        return x / y

    def power(self, x, y):
        try:
            return math.pow(x, y)
        except OverflowError:
            raise ValueError("Error: Result too large!")

    @staticmethod
    def sin(x):
        return math.sin(math.radians(x))

    @staticmethod
    def cos(x):
        return math.cos(math.radians(x))

    @staticmethod
    def tan(x):
        angle_rad = math.radians(x)
        # Check for undefined values (90°, 270°, etc.)
        if abs(x % 180) == 90:
            raise ValueError("Error: Tangent is undefined at this angle!")
        return math.tan(angle_rad)

    @staticmethod
    def sqrt(x):
        if x < 0:
            raise ValueError("Error: Cannot calculate square root of negative number!")
        return math.sqrt(x)