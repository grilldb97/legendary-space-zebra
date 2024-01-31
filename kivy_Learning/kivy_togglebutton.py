from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class WidgetsExample(GridLayout):

    def on_toggle_button_state(self, widget):
        print("toggle state: " + widget.state)
        if widget.state == "normal":
            widget.text = "OFF"
        else:
            widget.text = "ON"


class ToggleButtonApp(App):
    pass


if __name__ == '__main__':
    ToggleButtonApp().run()
