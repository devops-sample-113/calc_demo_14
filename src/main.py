# main.py
import flet as ft
import math
from calculate import Calculator
from buttons import DigitButton, OperatorButton, ActionButton

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()
        self.result = ft.Text(
            value="0",
            color=ft.colors.WHITE,
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.RIGHT,
        )
        self.calc = Calculator()
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.expand = 1
        self.content = self.build_ui()

    def build_ui(self):
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[self.result],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    padding=10,
                    margin=ft.margin.only(bottom=20)
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="sin", button_clicked=self.button_clicked, action="sin"),
                        ActionButton(text="cos", button_clicked=self.button_clicked, action="cos"),
                        ActionButton(text="tan", button_clicked=self.button_clicked, action="tan"),
                        ActionButton(text="π", button_clicked=self.button_clicked, action="pi"),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="AC", button_clicked=self.button_clicked, action="clear"),
                        ActionButton(text="+/-", button_clicked=self.button_clicked, action="negate"),
                        ActionButton(text="%", button_clicked=self.button_clicked, action="percent"),
                        OperatorButton(text="÷", button_clicked=self.button_clicked, operations="div"),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked, value=7),
                        DigitButton(text="8", button_clicked=self.button_clicked, value=8),
                        DigitButton(text="9", button_clicked=self.button_clicked, value=9),
                        OperatorButton(text="×", button_clicked=self.button_clicked, operations="mul"),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked, value=4),
                        DigitButton(text="5", button_clicked=self.button_clicked, value=5),
                        DigitButton(text="6", button_clicked=self.button_clicked, value=6),
                        OperatorButton(text="-", button_clicked=self.button_clicked, operations="sub"),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked, value=1),
                        DigitButton(text="2", button_clicked=self.button_clicked, value=2),
                        DigitButton(text="3", button_clicked=self.button_clicked, value=3),
                        OperatorButton(text="+", button_clicked=self.button_clicked, operations="add"),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="0", button_clicked=self.button_clicked, value=0, expand=2),
                        DigitButton(text=".", button_clicked=self.button_clicked, value="."),
                        ActionButton(text="=", button_clicked=self.button_clicked, action="calculate"),
                    ]
                ),
                ft.Row(
                    controls=[
                        ActionButton(text="√", button_clicked=self.button_clicked, action="sqrt"),
                        ActionButton(text="^", button_clicked=self.button_clicked, action="pow"),
                        ActionButton(text="⌫", button_clicked=self.button_clicked, action="backspace"),
                    ]
                ),
            ],
            spacing=10
        )

    def button_clicked(self, e):
        data_type = e.control.type
        if data_type == "digit":
            self.digit_button_clicked(e)
        elif data_type == "operator":
            self.operator_button_clicked(e)
        elif data_type == "action":
            self.action_button_clicked(e)
        self.update()

    def digit_button_clicked(self, e):
        value = e.control.value
        if value == "." and "." in self.result.value:
            return  # Prevent multiple decimal points
        
        if self.result.value == "0" or self.new_operand:
            self.result.value = "." if value == "." else str(value)
            self.new_operand = False
        else:
            self.result.value = self.result.value + str(value)

    def operator_button_clicked(self, e):
        if self.result.value.endswith('.'):
            self.result.value = self.result.value[:-1]
            
        self.operator = e.control.operations
        try:
            if self.operand1 is not None:
                self.result.value = str(
                    self.calc.calculate(
                        float(self.operand1),
                        float(self.result.value),
                        self.operator
                    )
                )
            self.operand1 = float(self.result.value)
            self.new_operand = True
        except ValueError as err:
            self.result.value = str(err)
            self.reset()

    def action_button_clicked(self, e):
        action = e.control.action
        try:
            current_value = float(self.result.value)
            
            if action == "clear":
                self.reset()
                self.result.value = "0"
            elif action == "negate":
                self.result.value = str(-current_value)
            elif action == "percent":
                self.result.value = str(current_value / 100)
            elif action == "calculate":
                if self.operand1 is not None and self.operator:
                    self.result.value = str(
                        self.calc.calculate(
                            float(self.operand1),
                            current_value,
                            self.operator
                        )
                    )
                    self.reset()
            elif action == "backspace":
                if len(self.result.value) > 1:
                    self.result.value = self.result.value[:-1]
                else:
                    self.result.value = "0"
            elif action == "pi":
                self.result.value = str(math.pi)
                self.new_operand = True
            elif action == "sqrt":
                self.result.value = str(self.calc.sqrt(current_value))
            elif action == "pow":
                self.operator = "pow"
                self.operand1 = current_value
                self.new_operand = True
            elif action in ["sin", "cos", "tan"]:
                func = getattr(self.calc, action)
                self.result.value = str(func(current_value))
            
        except ValueError as err:
            self.result.value = str(err)
        except Exception as err:
            self.result.value = "Error"
            print(f"Error: {err}")
        
    def reset(self):
        self.operator = None
        self.operand1 = None
        self.new_operand = True

def main(page: ft.Page):
    page.title = "Scientific Calculator"
    page.window_width = 400
    page.window_height = 600
    page.window_min_width = 400
    page.window_min_height = 600
    page.bgcolor = ft.colors.BLACK
    page.padding = 20
    
    calc = CalculatorApp()
    page.add(calc)

if __name__ == "__main__":
    ft.app(target=main)