import flet as ft
import math

# この辺は、CSSの指定みたいなことをしている？
class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    # application's root control (i.e. "view") containing all other controls
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="π", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="e", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="√", button_clicked=self.button_clicked
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="log", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="exp", button_clicked=self.button_clicked
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="sin", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="cos", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="tan", button_clicked=self.button_clicked
                        ),
                        
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ]
        )

    # UIの設定は以上
    # 以下から計算

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        # ボタンがクリックされた結果がdataに入る

        # 以下、それぞれのボタンが押された時の挙動を指示
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
            # エラー出たり、クリックされたボタンがACだったら、結果欄（resultは結果欄を指しているっぽい）には0を表示

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
                # 結果欄が0か初回入力なら、結果欄にはそのまま数字を入れる
            else:
                self.result.value = self.result.value + data
                # 初回入力じゃないなら、既に表示されている数字の隣に今入力された数字を表示する
                # 2桁以上の数字を表示したいときのため

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        elif data in ("sin", "cos", "tan"):
            try:
                # 入力された値をラジアンに変換して計算
                value_in_radians = math.radians(float(self.result.value))
                if data == "sin":
                    self.result.value = self.format_number(math.sin(value_in_radians))
                elif data == "cos":
                    self.result.value = self.format_number(math.cos(value_in_radians))
                elif data == "tan":
                    # tanの場合、90度（π/2ラジアン）のような値ではエラーを表示
                    if abs(value_in_radians % math.pi - math.pi / 2) < 1e-10:
                        self.result.value = "Error"
                    else:
                        self.result.value = self.format_number(math.tan(value_in_radians))
            except ValueError:
                self.result.value = "Error"
            self.reset()

        elif data in ("log", "exp"):
            try:
                if data == "log":
                    # logの場合、入力値が0以下だとエラー
                    if float(self.result.value) <= 0:
                        self.result.value = "Error"
                    else:
                        self.result.value = self.format_number(math.log(float(self.result.value)))
                elif data == "exp":
                    # expの場合、指数関数を計算
                    self.result.value = self.format_number(math.exp(float(self.result.value)))
            except ValueError:
                self.result.value = "Error"
            self.reset()
            
        elif data in ("π", "e", "√"):
            try:
                if data == "π":
                    self.result.value = self.format_number(math.pi)
                elif data == "e":
                    self.result.value = self.format_number(math.e)
                elif data == "√":
                    if float(self.result.value) < 0:
                        self.result.value = "Error"  # 負の数は平方根を計算できない
                    else:
                        self.result.value = self.format_number(math.sqrt(float(self.result.value)))
            except ValueError:
                self.result.value = "Error"
            
            self.reset()

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calc App"
    # create application instance
    calc = CalculatorApp()

    # add application's root control to the page
    page.add(calc)


ft.app(target=main)

