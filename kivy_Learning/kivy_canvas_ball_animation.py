from kivy.app import App
from kivy.graphics import Ellipse
from kivy.metrics import dp
import kivy.properties
from kivy.uix.widget import Widget


class CanvasExample(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = dp(60)
        self.vx = dp(3)
        self.vy = dp(3)
        with self.canvas:
            self.ball = Ellipse(pos=self.center, size=(self.ball_size, self.ball_size))
        kivy.properties.Clock.schedule_interval(self.update, 1 / 60)

    def on_size(self, *args):
        self.ball.pos = (self.center_x-self.ball_size/2, self.center_y-self.ball_size/2)

    def update(self, dt):
        x, y = self.ball.pos

        x += self.vx
        y += self.vy

        # self.ball_size / self.width
        # self.vx = -self.vx
        if y + self.ball_size > self.height:
            y = self.height-self.ball_size
            self.vy = -self.vy

        if x + self.ball_size > self.width:
            x = self.width-self.ball_size
            self.vx = -self.vx

        if y < 0:
            y = 0
            self.vy = -self.vy
        if x < 0:
            x = 0
            self.vx = -self.vx

        self.ball.pos = (x, y)


class CanvasBallAnimationApp(App):
    pass


if __name__ == '__main__':
    CanvasBallAnimationApp().run()
