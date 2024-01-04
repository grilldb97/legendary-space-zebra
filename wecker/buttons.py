from tkinter import *
from functions import ButtonFunctions
from spinboxes import Spinboxes
from help import HelpWindow
from alarm import AlarmManager
from global_state import global_state


class Buttons:
    def __init__(self, parent, alarm_manager=None):
        self.parent = parent
        self.spinbox_creator = Spinboxes()  # Erstellen Sie eine Instanz von SpinboxCreator

        # Erstellen Sie eine Instanz von ButtonFunctions ohne alarm_manager
        self.button_functions = ButtonFunctions(None, self, self.spinbox_creator)

        # Erstellen Sie eine Instanz von AlarmManager, wenn sie nicht übergeben wurde
        if alarm_manager is None:
            alarm_manager = AlarmManager(self, self.button_functions)

        # Weisen Sie die AlarmManager-Instanz der ButtonFunctions-Instanz zu
        self.button_functions.alarm_manager = alarm_manager

        self.help_window = HelpWindow()
        self.alarm_manager = alarm_manager
        self.wecker = self.button_functions
        self.wecker_set = False
        self.stunden_spinboxes = []  # Erstellen Sie die Liste hier
        self.minuten_spinboxes = []  # Erstellen Sie die Liste hier

    def button_wecker_stellen(self, tab_control, wecker_index):
        self.button_wecker_stellen_obj = Button(self.parent, text="stellen",
                                                width=6, command=lambda index=wecker_index: self.button_functions.
                                                function_stellen(tab_control.index(tab_control.select())))
        self.button_wecker_stellen_obj.place(relx=0.420, rely=0.400, anchor=CENTER)

    def button_delete(self):
        self.delete_button_obj = Button(self.parent, text="löschen", width=6,
                                        command=self.button_functions.function_delete, state='disabled')
        self.delete_button_obj.place(relx=0.420, rely=0.650, anchor=CENTER)
        return self.delete_button_obj

    def button_snooze(self):
        state = global_state.get_state()
        self.button_snooze_obj = Button(self.parent, text="Snooze",
                                        command=self.button_functions.function_snooze, state=state)
        self.button_snooze_obj.place(relx=0.500, rely=0.300)
        self.button_snooze_obj.config(bg="blue", fg="white", anchor=CENTER)
        return self.button_snooze_obj

    def button_stop(self):
        state = global_state.get_state()
        self.button_stop_obj = Button(self.parent, text="Stop",
                                      command=self.button_functions.function_stop, state=state)
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

    '''def update_button_states(self, wecker_index):
        # Aktualisieren Sie den Zustand der "Stop" und "Snooze" Schaltflächen basierend auf dem Alarmzustand
        state = NORMAL if global_state.get_state(wecker_index) else DISABLED
        print(f"Updating button states to {state}")  # Debugging-Ausgabe
        self.alarm_manager.window.after(0, self.button_stop(wecker_index).config, {'state': state})
        self.alarm_manager.window.after(0, self.button_snooze(wecker_index).config, {'state': state})'''

    def create_time_frame(self, parent, wecker_index):
        # Erstellen Sie die Spinboxen für Stunden und Minuten
        spinbox_stunden, spinbox_minuten = self.spinbox_creator.create_spinboxes(parent, wecker_index)

        # Erstellen Sie einen Frame, um die Spinboxen zu halten
        frame = Frame(parent)
        frame.pack(side=TOP)  # Positionieren Sie den Frame am oberen Rand des Tabs

        # Positionieren Sie die Spinboxen im Frame
        spinbox_stunden.pack(side=LEFT, padx=(150, 0), anchor='n')
        spinbox_minuten.pack(side=LEFT, padx=(0, 150), anchor='n')
