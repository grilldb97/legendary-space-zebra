from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget


class CanvasExample(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0, 1, 0)
            self.rect = Rectangle(pos=(500, 200), size=(150, 100))

    def on_button_a_click(self):
        x, y = self.rect.pos
        w, h = self.rect.size
        inc = dp(10)

        diff = self.width - (x + w)
        if diff < inc:
            inc = diff

        x += inc
        self.rect.pos = (x, y)


class CanvasMoveRectangleApp(App):
    pass


if __name__ == '__main__':
    CanvasMoveRectangleApp().run()
