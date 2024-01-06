import queue
import threading
from datetime import datetime
import time
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
        self.alarm_sound = AlarmSound()
        # Erstellen Sie eineWarteschlange für jeden Wecker
        self.alarm_queues_tabs = [queue.Queue() for _ in range(len(self.wecker_liste))]
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

        # Starten Sie den AlarmManager in einem neuen Thread
        Threads.start_alarm_manager(alarm_manager)

    def show_window(self):
        self.window.title("WECKER")
        self.window.geometry("400x250")  # Vergrößert das Fenster
        self.window.resizable(False, False)  # Verhindert das Ändern der Fenstergröße
        self.window.attributes('-toolwindow', True)  # Blendet den Maximierung-Button aus
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

    def create_tab(self, tab_control, wecker_index, alarm_queue_tab):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=f"Wecker {wecker_index + 1}")
        # Erstellen Sie eine Buttons-Instanz für das aktuelle Tab
        buttons = Buttons(tab, None)
        # Fügen Sie die alarm_queue dieses Tabs zur Buttons-Instanz hinzu
        buttons.alarm_queue_tab = alarm_queue_tab
        self.buttons.append(buttons)
        # Erstellen Sie das Zeitfenster und zeigen Sie die Schaltflächen an
        buttons.create_time_frame(tab, wecker_index)
        self.show_buttons(tab_control)  # Übergeben Sie wecker_index an die show_buttons-Methode

    def start_alarm(self, buttons, wecker_index, alarm_queue_tab):
        print("start_alarm")
        while True:
            if not alarm_queue_tab.empty():
                alarm_event = alarm_queue_tab.get()
                if alarm_event['wecker_index'] == wecker_index and alarm_event['is_playing']:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    while alarm_event['alarm_time'] != current_time:
                        time.sleep(1)
                        current_time = now.strftime("%H:%M")
                    print("hier")
                    self.alarm_sound = AlarmSound
                    self.button_stop = Buttons.button_stop
                    self.button_snooze = Buttons.button_snooze
                    mp3_path = alarm_event['mp3_path']
                    mode = alarm_event['mode']
                    alarm_thread = threading.Thread(target=self.alarm_sound.run_play,
                                                    args=(mode, mp3_path))
                    alarm_thread.daemon = True
                    alarm_thread.start()
            time.sleep(1)

    def start_alarm_thread(self, wecker_index, alarm_queue_tab):
        start_alarm = MainWindow.start_alarm
        alarm_thread = threading.Thread(target=start_alarm, args=(self.alarm_sound, self.buttons,
                                                                  wecker_index, alarm_queue_tab))
        alarm_thread.start()

    def show_tabs(self, wecker_liste):
        tab_control = ttk.Notebook(self.window)
        tab_control.grid(row=1, column=1, pady=10, sticky='nsew')

        for wecker_index in wecker_liste:
            # Holen Sie die alarm_queue für diesen Tab
            alarm_queue_tab = self.alarm_queues_tabs[wecker_index]
            # Übergeben Sie die alarm_queue als Parameter an create_tab
            self.create_tab(tab_control, wecker_index, alarm_queue_tab)
            # Starten Sie einen neuen Thread für diesen Tab
            self.start_alarm_thread(wecker_index, alarm_queue_tab)

    def show_time(self):
        time_label = StringVar()
        time_label.set('00:00:00')
        label = Label(self.window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
        label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu
        Threads.start_uhrzeit(time_label)

    def show_buttons(self, tab_control):
        for buttons in self.buttons:
            buttons.button_stop(tab_control)
            buttons.button_snooze(tab_control)
            buttons.button_wecker_stellen(tab_control)
            buttons.button_delete()
            buttons.button_change_alarm_musik()
