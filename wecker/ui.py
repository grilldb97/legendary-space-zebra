import alarms
from datetime import datetime
from tkinter import *
import threading
from functools import partial
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from threading import Thread


class GUI:
    def __init_(self):
        # Erstelle die Alarmobjekte
        self.alarms = [alarms.Alarm(i, alarm_manager=i) for i in range(3)]

        # Starte die Alarmthreads
        alarms.AlarmManager.start_alarm_manager()

        # Richte einen Listener für das Setzen des Alarms ein
        self.set_alarm_listener()

        # Erstelle einen Listener für das Setzen des Alarms
        self.set_alarm_event = Event()

    @staticmethod
    def start(create_window):
        # Erstelle das Fenster
        create_window()
        # Starte den Hauptloop des Fensters
        mainloop()
    def set_alarm_listener(self):
        # Richte einen Listener für das Drücken des Set-Alarm-Buttons ein
        for tab in self.tabs:
            tab.set_alarm_button.bind("<Button-1>", lambda event: self.set_alarm())

        # Richte einen Listener für das Setzen des Alarms über die Spinboxes ein
        for i in range(3):
            self.stunden_spinboxes[i].bind("<ButtonRelease-1>", lambda event: self.set_alarm())
            self.minuten_spinboxes[i].bind("<ButtonRelease-1>", lambda event: self.set_alarm())

    @staticmethod
    def on_set_alarm():
        alarms.AlarmThreadManager.schedule_alarm()

    def set_alarm(self):
        # Lies die Werte aus den Spinboxes
        hours = self.stunden_spinboxes[self.active_tab].get()
        minutes = self.minuten_spinboxes[self.active_tab].get()

        # Erstelle einen neuen Alarm-Thread
        alarm = alarms.Alarm(self.active_tab, hours, minutes)

        # Übergebe den Alarm-Thread an den Alarmmanager
        self.alarm_manager.schedule_alarm(alarm)


class MyWindow:

    def __init__(self, alarm_objects, queue, threads):
        self.window = None
        self.alarms = alarm_objects
        self.alarm_queue = queue
        self.alarm_threads = threads
        self.tabs = []
        self.stunden_spinboxes = [None, None, None]
        self.minuten_spinboxes = [None, None, None]

        self.create_window()

    def create_window(self, window):
        time_label = Label(self.window, textvariable=self.time_label, font=("Helvetica", 30, "bold"), fg="green")
        time_label.grid(row=0, column=1, pady=10)

        uhrzeit_thread = threading.Thread(target=self.uhrzeit, args=(time_label,))
        uhrzeit_thread.start()

        alarm_manager_thread = threading.Thread(target=self.alarm_threads[0].
                                                alarm_manager, args=(self.alarm_queue, self.alarm_threads))
        alarm_manager_thread.start()

        tab_control = ttk.Notebook(self.window)
        tab_control.grid(row=1, column=1, pady=10, sticky='nsew')  # Fügt vertikalen Abstand hinzu

        for i in range(3):
            self.create_tab(tab_control, i)

        help_button = Button(self.window, text="?", command=self.open_help_window)
        help_button.place(relx=1, x=-2, y=2, anchor=NE)

        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(1, weight=1)

    def uhrzeit(self, time_label):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_label.set(current_time)
        self.window.after(1000, self.uhrzeit, time_label)  # Planen Sie die nächste Aktualisierung in 1 Sekunde

    def create_tab(self, tab_control, index):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=f"Wecker {index + 1}")
        self.tabs.append(tab)  # Fügen Sie den erstellten Tab zur Liste hinzu

        time_frame = Frame(tab)
        time_frame.place(relx=0.502, rely=0.1, anchor=CENTER)

        # Create the spinboxes for hours and minutes
        stunden_spinbox = self.create_spinbox(time_frame, 0, 23)
        minuten_spinbox = self.create_spinbox(time_frame, 0, 59)

        # Insert the spinboxes into the lists
        self.stunden_spinboxes.append(stunden_spinbox)
        self.minuten_spinboxes.append(minuten_spinbox)

        self.create_button(tab, "Wecker stellen", partial(
            self.alarms[index].set_wecker_zeit, self.stunden_spinboxes, self.minuten_spinboxes), 0.400, 0.4)

        snooze_button = self.create_button(tab, "Snooze", partial(self.alarms[index].snooze,
                                                                  self.alarm_queue), 0.605, 0.4)
        snooze_button.config(bg="blue", fg="white")

        stop_button = self.create_button(tab, "Stop", partial(
            self.alarms[index].stop_alarm, index, self.stunden_spinboxes,
            self.minuten_spinboxes, self.alarm_threads), 0.705, 0.4)
        stop_button.config(bg="red", fg="white")

        self.create_button(tab, "Wecker löschen", partial(
            self.alarms[index].delete_alarm, index, self.stunden_spinboxes,
            self.minuten_spinboxes, self.button_labels), 0.400, 0.7)

        button = Button(tab, textvariable=self.button_labels[index],
                        command=partial(self.alarms[index].wechsel_alarm_typ), width=10)
        button.place(relx=0.650, rely=0.7, anchor=CENTER)
