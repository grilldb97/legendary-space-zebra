from tkinter import Spinbox, StringVar
import time
from datetime import datetime
import threading
from tkinter import filedialog
from alarm import AlarmManager
from datetime import datetime, timedelta


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
    def function_delete(self):
        print("delete")

    def function_stellen(self, index, stunden_spinbox, minuten_spinbox):
        stunden = stunden_spinbox.get()
        minuten = minuten_spinbox.get()
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

    def function_change(self):
        if self.change_button_text.get() == "Alarm":
            self.alarm_on = True  # Setzen Sie die Variable, die angibt, dass ein Alarm ausgegeben werden soll
        elif self.change_button_text.get() == "Musik":
            self.waehle_musik()  # Wählen Sie eine MP3-Datei aus
            if self.musik_dateien != "nonexistent.mp3":  # Überprüfen Sie, ob eine Musikdatei ausgewählt wurde
                self.change_button_text.set("Musik")
                self.alarm_on = False  # Setzen Sie die Variable, die angibt, dass ein Alarm ausgegeben werden soll, auf False
            else:
                self.change_button_text.set("Alarm")

    def waehle_musik(self):
        self.musik_dateien = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])


class Uhrzeit:
    def uhrzeit(self, time_label):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_label.set(current_time)
            time.sleep(1)
