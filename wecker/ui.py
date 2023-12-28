from datetime import datetime
from tkinter import *
import threading
from functools import partial
from tkinter import ttk
from tkinter import StringVar
from alarms import Alarm

alarm = Alarm()
class Window:

    button_labels = [StringVar(Window.window, value="Alarm") for _ in range(3)]
    window = Tk()
    window.title("WECKER")
    window.geometry("400x250")
    window.resizable(False, False)
    window.attributes('-toolwindow', True)

    def __init__(self, alarm_objects, queue, threads):
        self.alarms = alarm_objects
        self.alarm_queue = queue
        self.alarm_threads = threads
        self.time_label = StringVar()
        self.time_label.set("00:00:00")
        self.tabs = []
        self.stunden_spinboxes = [None, None, None]
        self.minuten_spinboxes = [None, None, None]

        self.alarms = alarm_objects
        self.alarm_queue = queue
        self.alarm_threads = threads
        self.create_window()

    @staticmethod
    def create_spinbox(time_frame, from_, to):
        if from_ == to:
            return None
        return Spinbox(time_frame, from_=from_, to=to)

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

        # Position the spinboxes in their respective frames
        stunden_spinbox.grid(row=0, column=0)
        minuten_spinbox.grid(row=0, column=1)
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

    @staticmethod
    def create_button(tab, text, command, relx, rely):
        button = Button(tab, text=text, command=command)
        button.place(relx=relx, rely=rely, anchor=CENTER)
        return button

    @staticmethod
    def open_help_window():
        help_window = Toplevel()
        help_window.title("Hilfe")
        Label(help_window, text="Hier sind die Anweisungen...").pack()

    def create_window(self):
        time_label = Label(self.window, textvariable=self.time_label, font=("Helvetica", 30, "bold"), fg="green")
        time_label.grid(row=0, column=1, pady=10)

        uhrzeit_thread = threading.Thread(target=self.uhrzeit, args=(time_label,))
        uhrzeit_thread.start()

        alarm_manager_thread = threading.Thread(target=alarm_threads[0].
                                                alarm_manager, args=(alarm_queue, alarm_threads))
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

    @staticmethod
    def mainloop():
        pass
        mainloop()