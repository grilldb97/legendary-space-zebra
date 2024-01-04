from tkinter import *
from tkinter import ttk
from alarm import AlarmManager, AlarmSound
from buttons import Buttons
from functions import Threads, ButtonFunctions
from help import HelpWindow
from spinboxes import Spinboxes


class MainWindow:
    def __init__(self):
        self.help_window = HelpWindow()
        self.window = Tk()
        self.wecker_liste = list(range(3))
        self.show_time()
        self.buttons = []
        self.show_tabs(self.wecker_liste)

        # Erstellen Sie eine separate Instanz von Buttons nur für den Hilfeknopf
        help_buttons = Buttons(self.window, None)
        help_buttons.button_help()

        # Erstellen Sie eine Instanz von Spinboxes
        self.spinbox_creator = Spinboxes()

        # Erstellen Sie eine Instanz von ButtonFunctions
        self.button_functions = ButtonFunctions(None, self, self.spinbox_creator)


        # Erstellen Sie eine Instanz von AlarmManager
        alarm_manager = AlarmManager(self.buttons, self.button_functions)

        self.alarm_sound = AlarmSound()

        # Starten Sie den AlarmManager in einem neuen Thread
        Threads.start_alarm_manager(alarm_manager)

    def show_window(self):
        self.window.title("WECKER")
        self.window.geometry("400x250")  # Vergrößert das Fenster
        self.window.resizable(False, False)  # Verhindert das Ändern der Fenstergröße
        self.window.attributes('-toolwindow', True)  # Blendet den Maximierungsbutton aus
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

    def create_tab(self, tab_control, wecker_index):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=f"Wecker {wecker_index + 1}")
        # Erstellen Sie eine Buttons-Instanz für das aktuelle Tab
        buttons = Buttons(tab, None)

        self.buttons.append(buttons)
        # Erstellen Sie das Zeitfenster und zeigen Sie die Schaltflächen an
        buttons.create_time_frame(tab, wecker_index)
        self.show_buttons(tab_control, wecker_index)  # Übergeben Sie wecker_index an die show_buttons-Methode

    def show_tabs(self, wecker_liste):
        tab_control = ttk.Notebook(self.window)
        tab_control.grid(row=1, column=1, pady=10, sticky='nsew')

        for wecker_index in wecker_liste:
            self.create_tab(tab_control, wecker_index)

    def show_time(self):
        time_label = StringVar()
        time_label.set('00:00:00')
        label = Label(self.window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
        label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu
        Threads.start_uhrzeit(time_label)

    def show_buttons(self, tab_control, wecker_index):
        for buttons in self.buttons:
            buttons.button_stop()
            buttons.button_snooze()
            buttons.button_wecker_stellen(tab_control, wecker_index)
            buttons.button_delete()
            buttons.button_change_alarm_musik()
