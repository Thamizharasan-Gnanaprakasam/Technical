from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

Builder.load_file("widget_examples.kv")

class ImageExamples(GridLayout):
    pass

class WidgetExamples(GridLayout):
    toggle_text = StringProperty("OFF")
    cnt_btn_disable = BooleanProperty(True)
    cnt_lbl_text = StringProperty("0")
    slide_disable = BooleanProperty(False)
    counter: int = 0
    def on_toggle_click(self,toggle_btn: ToggleButton):
        if toggle_btn.state == "down":
            self.toggle_text = "ON"
            self.cnt_btn_disable = False
        else:
            self.toggle_text = "OFF"
            self.cnt_btn_disable = True

    def on_button_click(self):
        self.counter += 1
        self.cnt_lbl_text = str(self.counter)

    def on_switch_click(self, switch: Switch):
        self.slide_disable = switch.active

    def on_text_enter(self, textinp: TextInput):
        self.ids.Label1.text = textinp.text

    def test(self,textinp: Image):
        pass


    def on_slider_change(self):
        pass


class WidgetApp(App):
    def build(self,**kwargs):
        return ImageExamples()

if __name__ == "__main__":
    WidgetApp().run()