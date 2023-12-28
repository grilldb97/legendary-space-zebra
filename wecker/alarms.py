import time
from datetime import datetime
from tkinter import filedialog
import threading
import winsound
import pygame
import os
from tkinter import StringVar
snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion

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

    def set_alarm_time(hours, minutes):
        if not valid_time(hours, minutes):
            print("Invalid time")
            return

            # Set alarm time
    def valid_time(hours, minutes):
         # Check if valid
        return True/False

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