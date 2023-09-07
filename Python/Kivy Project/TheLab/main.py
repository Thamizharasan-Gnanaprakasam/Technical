from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

from canvas_examples import *

#Builder.load_file("TheLabApp.kv")


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CanvasWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_button_press(self, btn: Button):
        self.ids["Box1"].height=1000
        print(self.ids["Box1"].size)
        print(self.ids["Stack1"].size)
        self.ids["Box1"].clear_widgets()
        if btn.text == "Example 1":
            self.ids["Box1"].add_widget(CanvasExample1())
        elif btn.text == "Example 2":
            self.ids["Box1"].add_widget(CanvasExample2())
        elif btn.text == "Example 3":
            self.ids["Box1"].add_widget(CanvasExample3())
        elif btn.text == "Example 4":
            self.ids["Box1"].add_widget(CanvasExample4())
        elif btn.text == "Example 5":
            self.ids["Box1"].add_widget(CanvasExample5())
        elif btn.text == "Example 6":
            self.ids["Box1"].add_widget(CanvasExample6())
        elif btn.text == "Example 7":
            self.ids["Box1"].add_widget(CanvasExample7())

class MainMenu(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class TheLabApp(App):
    def build(self, **kwargs):
        sm = ScreenManagement(transition=RiseInTransition())
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(CanvasWindow(name="canvas"))
        return sm


TheLabApp().run()
