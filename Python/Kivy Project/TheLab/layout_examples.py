from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

Builder.load_file("layout_examples.kv")

class PageLayoutExample(PageLayout):
    pass

class ScrollViewExample(ScrollView):
    pass

class StackLayoutExample(StackLayout):
    btn_size=dp(100)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.orientation = "lr-tb"
        for i in range(100):
            btn = Button(text=str(i+1),size_hint=[None, None],size=[self.btn_size,self.btn_size])
            self.add_widget(btn)




class GridLayoutExample(GridLayout):
    pass

class AnchorLayoutExample(AnchorLayout):
    pass

class BoxLayoutExample(BoxLayout):
    def on_button_click(self,txt: str):
        self.orientation = txt.lower()

class MainWidgetExample(Widget):
    pass

class LayoutApp(App):
    def build(self):
        return PageLayoutExample()


if __name__ == "__main__":
    LayoutApp().run()