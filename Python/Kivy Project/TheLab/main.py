import importlib
import inspect
import math

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.uix.stacklayout import StackLayout

import canvas_examples
import widget_examples
import layout_examples

#Builder.load_file("TheLabApp.kv")


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LayoutWindow(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


        self.box1 = BoxLayout(orientation = "vertical")
        self.stack1 = StackLayout(orientation = "lr-tb")
        self.stack1.size_hint=[1,.2]
        self.stack1.spacing = dp(10)

        self.box2 = BoxLayout()


        self.classes = [obj for _,obj in inspect.getmembers(layout_examples,predicate=inspect.isclass)
                        if obj.__module__ == "layout_examples"]

        self.btn_wdth = math.floor(100/len(self.classes))/100
        self.class_dist = {}

        for i in self.classes:
            btn = Button()
            btn.size_hint = [self.btn_wdth, 1]
            self.stack1.add_widget(btn)
            btn.bind(on_press = self.on_button_click)

            if i.__name__ == "LayoutApp":
                btn.text = "Main Menu"
                self.class_dist[btn.text] = "self.manager.current = 'menu'"
            else:
                btn.text = i.__name__
                self.class_dist[btn.text] = "self.box2.add_widget(" + i.__module__ + "." + i.__name__ + "())"

        self.box1.add_widget(self.stack1)
        self.box1.add_widget(self.box2)
        self.add_widget(self.box1)

    def on_button_click(self,obj: Button):
        self.box2.clear_widgets()
        exec(self.class_dist[obj.text])

class WidgetWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.box1 = BoxLayout(orientation= "vertical")

        self.stack1 = StackLayout(orientation = "tb-rl")
        self.stack1.size_hint = [1, .2]
        self.stack1.spacing = dp(10)

        self.box2 =BoxLayout()

        self.classes = [obj for _,obj in inspect.getmembers(widget_examples,predicate=inspect.isclass)
                        if obj.__module__ == "widget_examples"]

        self.class_dict={}
        self.btn_wdth = math.floor(100/len(self.classes))/100


        for i in self.classes:
            btn = Button()
            btn.size_hint = [self.btn_wdth,1]
            btn.bind(on_press=self.onbutton_click)

            if i.__name__ == "WidgetApp":
                btn.text = "Main Menu"
                self.class_dict[btn.text] = "self.manager.current = 'menu'"
            else:
                btn.text = i.__name__
                self.class_dict[btn.text] = "self.box2.add_widget(" +  i.__module__ + "." + i.__name__ + "())"

            self.stack1.add_widget(btn)


        self.box1.add_widget(self.stack1)
        self.box1.add_widget(self.box2)
        self.add_widget(self.box1)

    def onbutton_click(self,obj):
        self.box2.clear_widgets()
        exec(self.class_dict[obj.text])

class CanvasWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box1 = BoxLayout(orientation="vertical")

        self.stack1 = StackLayout(orientation="lr-tb")
        self.stack1.size_hint = [1, .2]
        self.stack1.spacing = dp(10)

        self.box2 = BoxLayout()

        self.box1.add_widget(self.stack1)
        self.box1.add_widget(self.box2)
        self.add_widget(self.box1)

        self.classes = [obj for _,obj in inspect.getmembers(canvas_examples,predicate=inspect.isclass)
                        if  obj.__module__ == "canvas_examples"]
        self.class_dict={}
        self.var_size = (math.floor(100/len(self.classes))/100)


        for i in range(len(self.classes)):
            btn = Button()
            if self.classes[i].__name__.find("CanvasExample")>-1:
                btn.text=self.classes[i].__name__
                self.class_dict[btn.text] = "self.box2.add_widget(" + self.classes[i].__module__ + "." + self.classes[i].__name__ + "())"
            else:
                btn.text = "Main Menu"
                self.class_dict[btn.text] =  "self.parent.current = 'menu'"
            btn.bind(on_press = self.on_button_press)

            btn.size_hint=[self.var_size, 1]
            self.stack1.add_widget(btn)

    def on_button_press(self, obj):

        self.box2.clear_widgets()
        exec(self.class_dict[obj.text])

        #self.box2.add_widget(CanvasExample5())
        """
        print(btn_val)
        #self.ids["Box1"].height=1000
        #print(self.ids["Box1"].size)
        #print(self.ids["Stack1"].size)
        #self.ids["Box1"].clear_widgets()
        if btn_val == "Canvas 1":
            self.box2.add_widget(CanvasExample1())
        elif btn_val == "Canvas 2":
            self.box2.add_widget(CanvasExample1())
        elif btn_val == "Canvas 3":
            self.box2.add_widget(CanvasExample1())
        elif btn_val == "Example 4":
            self.box2.add_widget(CanvasExample1())
        elif btn_val == "Example 5":
            self.box2.add_widget(CanvasExample1())
        elif btn_val == "Example 6":
            self.box2.add_widget(CanvasExample1())
        elif btn_val == "Example 7":
            self.box2.add_widget(CanvasExample1())
        """

class MainMenu(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)


class TheLabApp(App):
    def build(self, **kwargs):
        sm = ScreenManagement(transition=RiseInTransition())
        sm.add_widget(MainMenu(name="menu"))
        sm.add_widget(CanvasWindow(name="canvas"))
        sm.add_widget(WidgetWindow(name="widgets"))
        sm.add_widget(LayoutWindow(name="layouts"))
        return sm


TheLabApp().run()
