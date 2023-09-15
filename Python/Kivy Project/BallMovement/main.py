from kivy.app import App
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp
from kivy.properties import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


class MainWidget(RelativeLayout):
    X_SPEED = 4
    Y_SPEED = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(50)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.ball = Ellipse(pos=self.center, size=[self.ball_size, self.ball_size])
            Clock.schedule_interval(self.move_ball, 1 / 60)

    def on_size(self, *args):
        self.ball.pos = [self.center_x - self.ball_size, self.center_y - self.ball_size]

    def move_ball(self, dt):
        x, y = self.ball.pos
        x_size, y_size = self.ball.size
        diff = self.width - (x + x_size)
        if diff < self.X_SPEED:
            x_pos = x + diff
        else:
            x_pos = x + self.X_SPEED

        diff = self.height - (y + y_size)

        if diff < self.Y_SPEED:
            y_pos = y + diff
        else:
            y_pos = y + self.Y_SPEED

        self.ball.pos = [x_pos, y_pos]

        if x_pos + x_size >= self.width or x_pos <= 0:
            self.X_SPEED *= -1

        if y_pos + y_size >= self.height or y_pos <= 0:
            self.Y_SPEED *= -1


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Screen1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box1 = BoxLayout()
        self.box1.add_widget(MainWidget())

        self.add_widget(self.box1)


class BallMovementApp(App):
    def build(self, **kwargs):
        sm = ScreenManagement()
        sm.add_widget(Screen1(name="Main1"))
        return sm


BallMovementApp().run()
