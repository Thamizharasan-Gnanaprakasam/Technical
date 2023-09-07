from kivy.app import App
from kivy.graphics import Line, Color, Rectangle, Ellipse
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

Builder.load_file("canvas_examples.kv")


class CanvasExample1(Widget):
    pass


class CanvasExample2(Widget):
    pass


class CanvasExample3(Widget):
    pass


# Move Rectangle
class CanvasExample4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Line(points=[dp(100), dp(100), dp(400), dp(500)], width=2)
            Color(r=1, g=0, b=0, a=1)
            Line(circle=[400, 200, 100])
            Line(rectangle=[800, 200, 100, 50])
            self.rect = Rectangle(pos=[100, 200], size=[100, 200])

    def on_button_click(self):
        x, y = self.rect.pos
        w, h = self.rect.size

        diff = self.width - (x + w)

        inc = dp(100)

        if (diff < inc):
            inc = diff

        x += inc
        self.rect.pos = (x, y)


# Ball Movement in Intervals
class CanvasExample5(Widget):
    xv = 4
    yv = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        with self.canvas:
            self.ball = Ellipse(pos=self.center, size=[self.ball_size, self.ball_size])
        Clock.schedule_interval(self.update, 1 / 60)

    def on_size(self, *args):
        self.ball.pos = [self.center_x - self.ball_size / 2, self.center_y - self.ball_size / 2]

    def update(self, dt):
        x, y = self.ball.pos
        radius_x, radius_y = self.ball.size

        if self.xv > 0:
            diff = self.width - (x + radius_x)
        else:
            diff = x + self.xv
        if (diff < self.xv):
            x += diff
            self.xv = -self.xv
        else:
            x += self.xv

        if self.yv > 0:
            diff = self.height - (y + radius_y)
        else:
            diff = y + self.yv
        if (diff < self.yv):
            y += diff
            self.yv = -self.yv
        else:
            x += self.xv
        self.ball.pos = (x, y + self.yv)


class CanvasExample6(Widget):
    pass


class CanvasExample7(BoxLayout):
    pass

class CanvasApp(App):
    def build(self):
        return CanvasExample7()

if __name__ == "__main__":
    CanvasApp().run()