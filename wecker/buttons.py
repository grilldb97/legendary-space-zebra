from tkinter import *
from functions import ButtonFunctions, SpinboxCreator
from help import HelpWindow


class Buttons:
    def __init__(self, parent, alarm_manager):
        self.parent = parent
        self.spinbox_creator = SpinboxCreator()  # Erstellen Sie eine Instanz von SpinboxCreator
        self.button_functions = ButtonFunctions(
            alarm_manager, self, self.spinbox_creator)  # Übergeben Sie spinbox_creator an ButtonFunctions
        self.help_window = HelpWindow()
        self.alarm_manager = alarm_manager
        self.wecker = self.button_functions
        self.wecker_set = False
        self.stunden_spinboxes = []  # Erstellen Sie die Liste hier
        self.minuten_spinboxes = []  # Erstellen Sie die Liste hier


    def button_wecker_stellen(self, wecker_index):
        # Erstellen Sie den Button
        self.button_wecker_stellen_obj = Button(self.parent, text="stellen",
                                                width=6, command=lambda:
        self.button_functions.function_stellen(wecker_index))
        self.button_wecker_stellen_obj.place(relx=0.420, rely=0.400, anchor=CENTER)

    def button_delete(self):
        self.delete_button_obj = Button(self.parent, text="löschen", width=6,
                                        command=self.button_functions.function_delete, state='disabled')
        self.delete_button_obj.place(relx=0.420, rely=0.650, anchor=CENTER)
        return self.delete_button_obj

    def button_snooze(self, wecker_index):
        self.button_snooze_obj = Button(self.parent, text="Snooze",
                                        command=lambda:
                                        self.button_functions.function_snooze(wecker_index), state='disabled')
        self.button_snooze_obj.place(relx=0.500, rely=0.300)
        self.button_snooze_obj.config(bg="blue", fg="white", anchor=CENTER)
        return self.button_snooze_obj

    def button_stop(self):
        self.button_stop_obj = Button(self.parent, text="Stop", command=self.button_functions.function_stop, state='disabled')
        self.button_stop_obj.place(relx=0.500, rely=0.300, x=49.5)
        self.button_stop_obj.config(bg="red", fg="white", anchor=CENTER)
        return self.button_stop_obj

    def button_change_alarm_musik(self):
        if not self.wecker_set:  # Überprüfen Sie, ob ein Wecker gesetzt ist
            self.button_change_alarm_musik_obj = Button(self.parent, textvariable=self.button_functions.
                                                        change_button_text, width=11,
                                                        command=self.button_functions.function_change)
            self.button_change_alarm_musik_obj.place(relx=0.605, rely=0.650, anchor=CENTER)

    def button_help(self):
        self.button_help_obj = Button(self.parent, text="?", command=self.help_window.help_content)
        self.button_help_obj.place(relx=1, x=-2, y=2, anchor=NE)

    def create_time_frame(self, parent, wecker_index):
        spinbox_creator = SpinboxCreator()
        # Erstellen Sie die Spinboxen für Stunden und Minuten
        stunden_spinbox = spinbox_creator.create_spinbox(
            parent, 0, 0,  23, 0, 0, wecker_index)
        minuten_spinbox = spinbox_creator.create_spinbox(
            parent, 0, 0, 59, 0, 0, wecker_index)

        # Speichern Sie die Spinboxen in den entsprechenden Attributen
        self.stunden_spinboxes[wecker_index] = stunden_spinbox
        self.minuten_spinboxes[wecker_index] = minuten_spinbox

        # Positionieren Sie die Spinboxen
        stunden_spinbox.place(relx=0.435, rely=0.1, anchor=CENTER)
        minuten_spinbox.place(relx=0.435, rely=0.1, x=45, anchor=CENTER)

