import math

from kivy.app import App
from kivy.config import Config
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput


# Builder.load_file("calculatorapp.kv")


# Config.set('graphics', 'borderless', 1)


class CalcWidget(BoxLayout):
    keypad = {
        "0": "icons/0.png",
        ".": "icons/icons8-stop-64.png",
        "=": "icons/equal.png",
        "1": "icons/1.png",
        "2": "icons/2.png",
        "3": "icons/3.png",
        "+": "icons/add.png",
        "4": "icons/4.png",
        "5": "icons/5.png",
        "6": "icons/6.png",
        "-": "icons/subtract.png",
        "7": "icons/7.png",
        "8": "icons/8.png",
        "9": "icons/9.png",
        "*": "icons/multiply.png",
        "AC": "icons/C.png",
        "+/-": "icons/plus_minus.png",
        "%": "icons/percent.png",
        "/": "icons/divide.png",
    }
    first_number = StringProperty("")
    operator = "+"
    second_number = StringProperty("")
    calc_bool = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        self.txt = TextInput()
        self.txt.text = "0"
        self.txt.multiline = False
        self.txt.size_hint = [1, 0.2]
        self.txt.input_filter = "float"
        self.txt.font_name = "fonts/Lcd.ttf"
        self.txt.font_size = dp(self.txt.height - 1)
        self.txt.focus = True
        self.txt.halign = "right"
        self.txt.valign = "top"

        self.stack = StackLayout()
        self.stack.orientation = "lr-bt"

        self.btn_width = math.floor(100 / 4) / 100
        self.btn_height = (self.stack.height / 4) / 100
        # print(self.height, self.txt.height)

        for i, v in self.keypad.items():
            btn = Button()
            # img = Image()
            # img.source = v

            btn.text = str(i)
            # btn.background_normal = v
            # btn.background_down= v
            if str(i) in ["=", "+", "-", "*", "/"]:
                btn.background_color = [250 / 255, 250 / 255, 51 / 255]
            elif str(i) not in ["AC", "+/-", "%"]:
                btn.background_color = [90 / 250, 90 / 255, 90 / 255]
            btn.size_hint = [self.btn_width, 0.2]
            # img.size_hint=[1, 1]
            if i == "0":
                btn.size_hint = [self.btn_width * 2, 0.2]
                # img.size_hint = [1, 1]
            btn.bind(on_press=self.on_button_click)
            # btn.add_widget(img)

            btn.font_name = "fonts/Lcd.ttf"
            btn.font_size = dp(40)

            self.stack.add_widget(btn)

            # self.stack.add_widget(img)
            # img.x = btn.x
            # img.y = btn.y
            # print(img.parent.pos_hint)
            # img.center_x = img.parent.center_x
            # img.center_y = img.parent.center_y
            # img.width=btn.width
            # img.height=btn.height
            # img.keep_ratio = False

        self.add_widget(self.txt)
        self.add_widget(self.stack)

    def on_button_click(self, obj: Button):
        if obj.text == "AC":
            self.txt.text = "0"
            self.first_number = ""
            self.second_number = ""
            # self.calc_bool = False
        elif obj.text in ["+", "-", "/", "*"]:
            if not self.calc_bool:
                self.first_number = ""
                self.second_number = ""

            if self.first_number == "" or not self.calc_bool:
                self.first_number = self.txt.text
            else:
                self.second_number = self.txt.text

            if self.second_number and self.first_number:
                self.first_number = self.format_txt(self.evaluate())
                self.txt.text = self.first_number
                # self.first_number = ""
                self.second_number = ""
            self.operator = obj.text
            self.calc_bool = False
        elif obj.text == "=":
            if self.second_number == "" and self.first_number != "":
                self.second_number = self.txt.text
            if self.first_number != "" and self.second_number != "":
                self.first_number = self.format_txt(self.evaluate())
                self.txt.text = self.first_number
            self.calc_bool = False
        elif obj.text == "+/-":
            self.txt.text = (
                "-" + self.txt.text if self.txt.text[0] != "-" else self.txt.text[1:]
            )
        elif obj.text == "%":
            self.txt.text = str(float(self.txt.text) / 100)
            self.calc_bool = False
        elif obj.text == ".":
            if self.calc_bool == False:
                self.txt.text = "0" + obj.text
            elif self.txt.text.find(".") == -1:
                self.txt.text += obj.text
            self.calc_bool = True
        else:
            if self.calc_bool == False or self.txt.text == "0":
                self.txt.text = ""
                self.calc_bool = True
            self.txt.text += obj.text

        self.txt.text = self.format_txt(self.txt.text)

    def evaluate(self) -> str:
        return str(
            eval(
                self.first_number.replace(",", "")
                + self.operator
                + self.second_number.replace(",", "")
            )
        )

    def format_txt(self, val: str):
        if val.find(".") > -1:
            return f"{float(val.replace(',','')):,}"
        else:
            return f"{int(val.replace(',','')):,}"


class Test(TextInput):
    # text = TextInput()
    # text.focus = True
    pass
    # txt = TextInput()
    # txt.walk_reverse()


class CalculatorApp(App):
    def build(self, **kwargs):
        Config.set("graphics", "width", "400")
        Config.set("graphics", "height", "600")
        Config.set("graphics", "resizable", 0)
        self.icon = "icons/calc.png"
        self.title = "Calculator"
        Config.write()
        return CalcWidget()


CalculatorApp().run()
