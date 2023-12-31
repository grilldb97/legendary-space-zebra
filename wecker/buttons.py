from tkinter import *
from functions import ButtonFunctions, SpinboxCreator
from help import HelpWindow


class Buttons:
    def __init__(self, parent, alarm_manager, button_functions):
        self.parent = parent
        self.button_functions = ButtonFunctions(alarm_manager)
        self.help_window = HelpWindow()
        self.alarm_manager = alarm_manager
        self.wecker = button_functions
    def button_wecker_stellen(self, index, stunden_spinbox, minuten_spinbox):
        self.button_wecker_stellen_obj = Button(self.parent, text="stellen", width=6,
                                                command=lambda: self.on_wecker_stellen(stunden_spinbox, minuten_spinbox))
        self.button_wecker_stellen_obj.place(relx=0.420, rely=0.400, anchor=CENTER)

    def on_wecker_stellen(self, stunden_spinbox, minuten_spinbox):
        stunden = stunden_spinbox.get()
        minuten = minuten_spinbox.get()
        # Fügen Sie die Weckerzeit direkt zum AlarmManager hinzu
        self.alarm_manager.add_alarm((stunden, minuten))
        # Deaktivieren Sie die Spinboxen
        SpinboxCreator.disable_spinboxes([stunden_spinbox, minuten_spinbox])
    def button_delete(self):
        self.delete_button_obj = Button(self.parent, text="löschen", width=6,
                                        command=self.button_functions.function_delete)
        self.delete_button_obj.place(relx=0.420, rely=0.650, anchor=CENTER)


    def button_snooze(self):
        self.button_snooze_obj = Button(self.parent, text="Snooze", command=self.button_functions.function_snooze)
        self.button_snooze_obj.place(relx=0.500, rely=0.300)
        self.button_snooze_obj.config(bg="blue", fg="white", anchor=CENTER)

    def button_stop(self):
        self.button_stop_obj = Button(self.parent, text="Stop", command=self.button_functions.function_stop)
        self.button_stop_obj.place(relx=0.500, rely=0.300, x=49.5)
        self.button_stop_obj.config(bg="red", fg="white", anchor=CENTER)

    def button_change_alarm_musik(self):
        if not self.wecker.wecker_set:  # Überprüfen Sie, ob ein Wecker gesetzt ist
            self.button_change_alarm_musik_obj = Button(self.parent, textvariable=self.button_functions.change_button_text,
                                                        width=11, command=self.button_functions.function_change)
            self.button_change_alarm_musik_obj.place(relx=0.605, rely=0.650, anchor=CENTER)
    def button_help(self):
        self.button_help_obj = Button(self.parent, text="?", command=self.help_window.help_content)
        self.button_help_obj.place(relx=1, x=-2, y=2, anchor=NE)
