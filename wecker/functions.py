from tkinter import Spinbox, StringVar
import time
from datetime import datetime
import threading
from tkinter import filedialog
from alarm import AlarmManager
from datetime import datetime, timedelta
import tkinter as tk


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
    def start_alarm_manager(alarm_manager):
        thread = threading.Thread(target=alarm_manager.run_alarms)
        thread.daemon = True
        thread.start()



class ButtonFunctions:
    def __init__(self, alarm_manager):
        self.change_button_text = StringVar()
        self.change_button_text.set("Alarm")
        self.wecker_zeit = None
        self.wecker_set = False
        self.alarm_on = False
        self.snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion
        self.alarm_manager = alarm_manager
        self.selected_mp3 = None  # Fügen Sie diese Zeile hinzu

    def function_delete(self):
        print("delete")

    def function_stellen(self, index, stunden_spinbox, minuten_spinbox):
        # Abrufen der Weckzeit aus den Spinboxen
        stunden = stunden_spinbox.get()
        minuten = minuten_spinbox.get()
        mode = self.get_current_mode()  # Rufen Sie die neue Methode hier auf
        mp3_path = self.selected_mp3  # Rufen Sie den Pfad zur ausgewählten MP3-Datei ab
        # Fügen Sie die Weckerzeit, den Modus und den MP3-Pfad direkt zum AlarmManager hinzu
        self.alarm_manager.add_alarm(index, stunden, minuten, mode, mp3_path)
        # Deaktivieren Sie die Spinboxen
        SpinboxCreator.disable_spinboxes([stunden_spinbox, minuten_spinbox])
    def function_snooze(self):
        if self.wecker_set:
            self.alarm_on = False
            # Konvertieren Sie die Weckerzeit in ein datetime-Objekt
            wecker_time = datetime.strptime(self.wecker_zeit, "%H:%M")
            # Fügen Sie 10 Minuten zur Weckerzeit hinzu
            snooze_time = (wecker_time + timedelta(minutes=10)).time()
            # Aktualisieren Sie die Weckerzeit
            self.wecker_zeit = snooze_time.strftime("%H:%M")
            # Aktualisieren Sie das Alarmereignis im AlarmManager
            self.alarm_manager.update_alarm(self.wecker_zeit)


    def function_stop(self):
        print("stop")

    def get_current_mode(self):
        return self.change_button_text.get()
    def function_change(self):
        if not self.alarm_on:  # Überprüfen Sie, ob der Alarm gesetzt ist
            self.waehle_musik()
            if self.selected_mp3:  # Überprüfen Sie, ob eine MP3-Datei ausgewählt wurde
                self.alarm_manager.set_selected_mp3(self.selected_mp3)  # Aktualisieren Sie den MP3-Pfad im AlarmManager
                self.change_button_text.set("Musik")
                self.alarm_on = True
            else:  # Wenn keine MP3-Datei ausgewählt wurde, bleibt der Modus auf "Alarm"
                self.change_button_text.set("Alarm")
                self.alarm_on = False

    def waehle_musik(self):
        self.selected_mp3 = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])

class Uhrzeit:
    def uhrzeit(self, time_label):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_label.set(current_time)
            time.sleep(1)
