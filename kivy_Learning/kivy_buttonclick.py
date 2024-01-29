from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class WidgetsExample(GridLayout):
    my_text = StringProperty("Hello")

    def on_button_click(self):
        print("Button clicked")
        self.my_text = "You clicked"


class ButtonClickApp(App):
    pass


if __name__ == '__main__':
    ButtonClickApp().run()
