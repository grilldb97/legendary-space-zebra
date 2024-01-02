from tkinter import Spinbox, StringVar
import time
from datetime import datetime
import threading
from tkinter import filedialog
from alarm import AlarmManager
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox


class SpinboxCreator:
    def __init__(self):
        self.values = {}  # Ein Wörterbuch zum Speichern der Spinbox-Werte
    @staticmethod
    def create_spinbox(self, parent, from_, to, row, colum, wecker_index):
        # Erstellen Sie eine StringVar, um den Wert der Spinbox zu speichern
        value = StringVar()
        value.set(from_)  # Setzen Sie den Anfangswert der Spinbox
        spinbox = Spinbox(from_=from_, to=to, width=5, textvariable=value)
        spinbox.grid(row=row, column=colum)  # Platziert in dem time_frame

        # Speichern Sie den Anfangswert in self.values
        if wecker_index not in self.values:
            self.values[wecker_index] = {}
        self.values[wecker_index]['stunden'] = value.get()

        # Aktualisieren Sie self.values jedes Mal, wenn der Wert geändert wird
        value.trace("w", lambda *args: self.values[wecker_index].update({'stunden': value.get()}))
        return spinbox

    def disable_spinboxes(self, wecker_index):
        # Deaktivieren Sie nur die Spinboxen, die zu einem bestimmten Wecker gehören
        self.values[wecker_index] = None


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
    def __init__(self, alarm_manager, buttons, spinbox_creator):
        self.change_button_text = StringVar()
        self.change_button_text.set("Alarm")
        self.wecker_zeit = None
        self.wecker_set = False
        self.alarm_on = False
        self.snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion
        self.alarm_manager = alarm_manager
        self.selected_mp3 = None  # Fügen Sie diese Zeile hinzu
        self.buttons = buttons
        self.spinbox_creator = spinbox_creator  # Speichern Sie eine Referenz auf die SpinboxCreator-Instanz
        self.alarm_times = {}
    def function_delete(self):
        print("delete")

    def function_stellen(self, wecker_index):
        # Überprüfen Sie, ob wecker_index in self.spinbox_creator.values ist, bevor Sie darauf zugreifen
        if wecker_index in self.spinbox_creator.values:
            stunden = self.spinbox_creator.values[wecker_index]['stunden']
            minuten = self.spinbox_creator.values[wecker_index]['minuten']
            alarm_time = f"{stunden}:{minuten}"
            print(f"Wecker {wecker_index + 1} Zeit: {alarm_time}")
            mp3_path = self.selected_mp3  # Rufen Sie den Pfad zur ausgewählten MP3-Datei ab
            mode = self.get_current_mode()  # Rufen Sie die neue Methode hier auf
            # Fügen Sie die Weckerzeit, den Modus und den MP3-Pfad direkt zum AlarmManager hinzu
            self.alarm_manager.add_alarm(wecker_index, alarm_time, mode, mp3_path)
            # Deaktivieren Sie die Spinboxen
            self.spinbox_creator.disable_spinboxes(wecker_index)
            self.buttons.button_delete().config(state='normal')
        else:
            print(f"Keine Spinboxen für wecker_index {wecker_index + 1} gefunden.")


    def function_snooze(self, wecker_index):
        if self.wecker_set:
            self.alarm_on = False
            self.alarm_manager.snooze_alarm(wecker_index)
            messagebox.showinfo("Snooze", "Der Wecker wurde um 10 Minuten verschoben.")


    def function_stop(self):
        self.alarm_manager.alarm_sound.stop_alarm()

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
