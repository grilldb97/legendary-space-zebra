from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout


class WidgetsExample(GridLayout):
    count = 1
    my_text = StringProperty("1")


    def on_button_click(self):
        self.count += 1
        self.my_text = str(self.count)



class ClickCounterApp(App):
    pass


if __name__ == '__main__':
    ClickCounterApp().run()
