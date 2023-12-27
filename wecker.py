import time
from datetime import datetime
from tkinter import *
from tkinter import filedialog
import threading
import winsound
from queue import Queue
from functools import partial
import pygame
import os
from tkinter import ttk
from tkinter import StringVar


class Alarm:
    alarm_zeit = ""
    stunden_spinboxes = []
    minuten_spinboxes = []

    def __init__(self, i, queue, threads):
        self.index = i
        self.alarm_on = False
        self.wecker_zeit = ""
        self.wecker_set = False
        self.alarm_typ = 0
        self.musik_dateien = "nonexistent.mp3"
        self.snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion
        self.alarm_queue = queue
        self.alarm_threads = threads
        self.button_labels = [StringVar(Window.window, value="Alarm") for _ in range(3)]
        alarms[i].button_labels = Window.button_labels

    def set_wecker_zeit(self, stunden, minuten):
        if self.is_valid_time(stunden, minuten):
            self.wecker_zeit = stunden + ":" + minuten
            self.wecker_set = True
        else:
            print("Bitte geben Sie eine gültige Zeit ein.")

    @staticmethod
    def is_valid_time(stunden, minuten):
        return (all(s.isdigit() for s in stunden) and
                all(m.isdigit() for m in minuten) and 0 <= int(stunden) < 24)

    def snooze(self):
        if self.wecker_set:
            self.alarm_on = False
            snooze_time_in_seconds = self.snooze_time * 60
            time.sleep(snooze_time_in_seconds)
            if not self.alarm_on:
                alarm_queue.put(self.index)

    def waehle_musik(self):
        self.musik_dateien = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])

    def alarm_mit_beep(self):
        self.alarm_on = True
        freq = 500
        while self.alarm_on:
            for _ in range(10):
                if not self.alarm_on:
                    break
                winsound.Beep(freq, 400)
                winsound.Beep(freq + 100, 150)
            time.sleep(1)

    def alarm_mit_musik(self):
        self.alarm_on = True
        pygame.mixer.init()
        if os.path.isfile(self.musik_dateien):
            pygame.mixer.music.load(self.musik_dateien)
            while self.alarm_on:
                pygame.mixer.music.play()
                time.sleep(1)
        else:
            # Wenn die Musikdatei nicht existiert, verwenden Sie den Standard-Alarmton
            self.alarm_mit_beep()

    def wechsel_alarm_typ(self):
        self.alarm_typ = 1 - self.alarm_typ

    def alarm_manager(self):
        while True:
            index = self.alarm_queue.get()
            while True:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                if self.wecker_zeit == current_time:
                    break
                time.sleep(1)
            self.alarm_threads[index] = threading.Thread(target=self.alarm, args=(index,))
            self.alarm_threads[index].daemon = True  # Mark the thread as a daemon
            self.alarm_threads[index].start()
            print(f"Alarm-Thread für Wecker {index+1} wurde gestartet")
            self.alarm_queue.task_done()

    def alarm(self, index):
        if self.alarm_on:
            if self.alarm_typ == 0:
                self.alarm_mit_beep()
            else:
                self.alarm_mit_musik()
            threading.Thread(target=self.start_blinking, args=(tabs[index],)).start()
            alarm_queue.put(index)
            while alarm_threads[index].is_alive():
                time.sleep(0.1)
            self.alarm_on = False
            alarm_threads[index].join()

    @staticmethod
    def blink(tab):
        current_color = tab.cget("background")  # Holt die aktuelle Hintergrundfarbe des Tabs
        next_color = "red" if current_color == "white" else "white"
        tab.config(background=next_color)  # Ändert die Hintergrundfarbe des Tabs

    @staticmethod
    def start_blinking(tab):
        current_color = tab.cget("background")
        next_color = "red" if current_color == "white" else "white"
        for _ in range(10):
            tab.config(background=next_color)
            time.sleep(1)
            next_color = "red" if next_color == "white" else "white"

    def stop_alarm(self, index, stunden_spinboxes, minuten_spinboxes):
        if self.wecker_set and index < len(self.stunden_spinboxes) and index < len(self.minuten_spinboxes):
            self.alarm_on = False
            if index < len(alarm_threads) and alarm_threads[index] is not None and alarm_threads[index].is_alive():
                alarm_threads[index].join()
            self.delete_alarm(index, stunden_spinboxes, minuten_spinboxes)  # Löscht den Wecker
            stunden_spinboxes[index].delete(0, 'end')
            minuten_spinboxes[index].delete(0, 'end')
            stunden_spinboxes[index].insert(0, '0')
            minuten_spinboxes[index].insert(0, '0')

    def delete_alarm(self, index, stunden_spinboxes, minuten_spinboxes):
        if self.wecker_set:
            self.alarm_on = False
            self.wecker_set = False
            stunden_spinboxes[index].delete(0, 'end')
            minuten_spinboxes[index].delete(0, 'end')
            stunden_spinboxes[index].insert(0, '0')
            minuten_spinboxes[index].insert(0, '0')
            stunden_spinboxes[index].config(state="normal")
            minuten_spinboxes[index].config(state="normal")
            button_labels[index].set("Alarm")
            self.alarm_typ = 0


# noinspection PyUnresolvedReferences
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


# Erstellen Sie die StringVar-Objekte hier, nachdem das Fenster erstellt wurde
global button_labels

# Erstellen Sie eine leere Liste von Tabs am Anfang Ihres Programms
tabs = []

snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion


if __name__ == "__main__":

    # Erstellen Sie eine globale Warteschlange
    alarm_queue = Queue()

    # Erstellen Sie eine Liste von Threads
    alarm_threads = [threading.Thread(target=lambda: None) for _ in range(3)]

    # Erstellen Sie Ihre Alarm-Objekte
    alarms = [Alarm(i, alarm_queue, alarm_threads) for i in range(3)]

    # Erstellen Sie eine Instanz der Window-Klasse
    window = Window(alarms, alarm_queue, alarm_threads)

    # Starten Sie die Alarm-Threads
    for thread in alarm_threads:
        thread.start()

    # Starten Sie den Hauptfenster-Thread
    Window.mainloop()
