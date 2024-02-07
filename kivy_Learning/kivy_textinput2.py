from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class WidgetsExample(GridLayout):
    text_input_str = StringProperty("foo")
    def on_text_validate(self, widget):
        self.text_input_str = widget.text


class TextInput2App(App):
    pass


if __name__ == '__main__':
    TextInput2App().run()
