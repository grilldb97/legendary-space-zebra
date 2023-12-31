from tkinter import Spinbox, StringVar
import time
from datetime import datetime
import threading
from alarm import Alarm, AlarmManager, AlarmThreadManager
from tkinter import filedialog


class SpinboxCreator:
    @staticmethod
    def create_spinbox(parent, from_, to, row, column):
        spinbox = Spinbox(parent, from_=from_, to=to, width=5)
        spinbox.grid(row=row, column=column)  # Platziert in dem time_frame
        return spinbox

    @staticmethod
    def disable_spinboxes(spinboxes):
        for spinbox in spinboxes:
            spinbox.config(state="disabled")


class Threads:
    @staticmethod
    def start_uhrzeit(time_label):
        uhr = Uhrzeit()
        thread = threading.Thread(target=uhr.uhrzeit, args=(time_label,))
        thread.daemon = True
        thread.start()
    @staticmethod
    def start_alarm_manager(alarm_manager, wecker):
        while True:
            if wecker.wecker_set and not any(alarm.wecker_zeit == wecker.wecker_zeit for alarm in alarm_manager.alarms):
                alarm = Alarm(len(alarm_manager.alarms))
                alarm.set_alarm_time(*wecker.wecker_zeit.split(":"))
                alarm_manager.add_alarm(alarm)
            time.sleep(1)


class ButtonFunctions:
    def __init__(self):
        self.wecker = Wecker()
        self.change_button_text = StringVar()
        self.change_button_text.set("Alarm")
        self.alarm_manager = AlarmManager()
        self.alarm_thread_manager = AlarmThreadManager(self.alarm_manager)
        self.wecker_zeit = None
        self.wecker_set = False
        self.alarm_on = False
        self.snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion

    def function_delete(self):
        print("delete")

    def function_stellen(self, index, stunden_spinbox, minuten_spinbox):
        stunden = stunden_spinbox.get()
        minuten = minuten_spinbox.get()
        self.wecker.set_wecker_zeit(stunden, minuten)
        alarm = Alarm(index)
        alarm.set_alarm_time(stunden, minuten)
        print(f"Alarm {index} erstellt mit Zeit {stunden}:{minuten}")
        self.alarm_manager.add_alarm(alarm)
        print(f"Alarm {index} zum AlarmManager hinzugefügt")
        # Deaktivieren Sie die Spinboxen
        SpinboxCreator.disable_spinboxes([stunden_spinbox, minuten_spinbox])

    def function_snooze(self):
        if self.wecker_set:
            self.alarm_on = False
            snooze_time_in_seconds = self.snooze_time * 60
            time.sleep(snooze_time_in_seconds)
            if not self.alarm_on:
                Threads.start_alarm_thread_manager()

    def function_stop(self):
        print("stop")

    def function_change(self):
        self.wecker.waehle_musik()  # Fügen Sie diese Zeile hinzu
        if self.wecker.musik_dateien != "nonexistent.mp3":  # Überprüfen Sie, ob eine Musikdatei ausgewählt wurde
            self.change_button_text.set("Musik")
        else:
            self.change_button_text.set("Alarm")


class Uhrzeit:
    def uhrzeit(self, time_label):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_label.set(current_time)
            time.sleep(1)


class Wecker:
    def __init__(self):
        self.wecker_zeit = None
        self.wecker_set = False
        self.alarm_on = False
        self.musik_dateien = "nonexistent.mp3"

    def set_wecker_zeit(self, stunden, minuten):
        if not self.wecker_set:
            if (stunden.isdigit() and minuten.isdigit() and 0 <= int(stunden) < 24
                    and 0 <= int(minuten) < 60):
                self.wecker_zeit = stunden + ":" + minuten
                self.wecker_set = True
                self.alarm_on = True
                # Starte den Wecker
                #Threads.start_alarm_manager(AlarmManager)
            else:
                print("Bitte geben Sie eine gültige Zeit ein.")
        else:
            print("Wecker ist bereits eingestellt.")

class Music:
    def __init__(self):
        self.musik_dateien = "nonexistent.mp3"

    def waehle_musik(self):
        self.musik_dateien = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])