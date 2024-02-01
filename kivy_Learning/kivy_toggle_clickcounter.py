from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.gridlayout import GridLayout


class WidgetsExample(GridLayout):
    count = 1
    count_enable = BooleanProperty(False)
    my_text = StringProperty("1")

    def on_toggle_button_state(self, widget):
        print("toggle state: " + widget.state)
        if widget.state == "normal":
            widget.text = "OFF"
            self.count_enable = False
        else:
            widget.text = "ON"
            self.count_enable = True

    def on_button_click(self):
        self.count += 1
        self.my_text = str(self.count)



class ToggleButtonClickApp(App):
    pass


if __name__ == '__main__':
    ToggleButtonClickApp().run()
