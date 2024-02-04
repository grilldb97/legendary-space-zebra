from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class WidgetsExample(GridLayout):

    def on_switch_active(self, widget):
        pass


class SwitchSliderApp(App):
    pass


if __name__ == '__main__':
    SwitchSliderApp().run()
