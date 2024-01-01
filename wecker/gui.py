from tkinter import *
from tkinter import ttk

from alarm import AlarmManager
from buttons import Buttons
from functions import ButtonFunctions
from functions import SpinboxCreator
from functions import Threads
from help import HelpWindow


class MainWindow:
    def __init__(self):
        self.help_window = HelpWindow()
        self.window = Tk()
        self.show_time()
        self.buttons = []
        self.show_tabs()

        # Erstellen Sie eine separate Instanz von Buttons nur für den Hilfeknopf
        help_button_functions = ButtonFunctions(None)
        help_buttons = Buttons(self.window, None, help_button_functions)
        help_buttons.button_help()


    def show_window(self):
        self.window.title("WECKER")
        self.window.geometry("400x250")  # Vergrößert das Fenster
        self.window.resizable(False, False)  # Verhindert das Ändern der Fenstergröße
        self.window.attributes('-toolwindow', True)  # Blendet den Maximierungsbutton aus
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)


    def show_tabs(self):
        tab_control = ttk.Notebook(self.window)
        tab_control.grid(row=1, column=1, pady=10, sticky='nsew')

        # Erstellen Sie eine separate Instanz von AlarmManager und ButtonFunctions für jedes Tab
        alarm_manager = AlarmManager()
        button_functions = ButtonFunctions(alarm_manager)

        for i in range(3):
            self.tab = ttk.Frame(tab_control)
            tab_control.add(self.tab, text=f"Wecker {i + 1}")

            # Erstellen Sie eine Buttons-Instanz für das aktuelle Tab und fügen Sie sie zur Liste hinzu
            buttons = Buttons(self.tab, alarm_manager, button_functions)
            self.buttons.append(buttons)

            # Erstellen Sie das Zeitfenster und zeigen Sie die Schaltflächen an
            buttons.create_time_frame(self.tab)
            self.show_buttons()

        # Starten Sie den AlarmManager, nachdem alle Tabs erstellt wurden
        Threads.start_alarm_manager(alarm_manager)


    def show_time(self):
        time_label = StringVar()
        time_label.set('00:00:00')
        label = Label(self.window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
        label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu
        Threads.start_uhrzeit(time_label)

    def show_buttons(self):
        for buttons in self.buttons:
            buttons.button_stop()
            buttons.button_snooze()
            for i in range(len(buttons.stunden_spinboxes)):
                buttons.button_wecker_stellen(i, buttons.stunden_spinboxes[i], buttons.minuten_spinboxes[i])
            buttons.button_delete()
            buttons.button_change_alarm_musik()

