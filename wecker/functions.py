import queue
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import filedialog

from matplotlib import pyplot as plt


class AlarmQueue:
    def __init__(self):
        self.alarm_queue_global = queue.Queue()


global_alarm_queue_instance = AlarmQueue()


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
        pass

    def function_stellen(self, wecker_index):
        if wecker_index in self.spinbox_creator.spinboxes:
            stunden, minuten = self.spinbox_creator.get_spinbox_values(wecker_index)
            alarm_time = f"{stunden}:{minuten}"
            mp3_path = self.selected_mp3
            mode = self.get_current_mode()
            # Fügen Sie das Alarm-Event zur globalen Warteschlange hinzu
            global_alarm_queue_instance.alarm_queue_global.put(
                {'wecker_index': wecker_index, 'alarm_time': alarm_time, 'mode': mode,
                 'mp3_path': mp3_path, 'is_playing': False})
            self.spinbox_creator.disable_spinboxes(wecker_index)
            self.buttons.button_delete().config(state='normal')
            self.buttons.button_wecker_stellen_obj.config(state='disabled')
        else:
            print(f"Kein Wecker mit Index {wecker_index} gefunden.")


    def function_stop(self):
        from alarm import AlarmManager
        self.button_functions = ButtonFunctions(None, self, self.spinbox_creator)
        alarm_manager = AlarmManager(self.buttons, self.button_functions)
        alarm_manager.stop_play()

    '''def update_button_states(self, wecker_index, parent):
        from buttons import Buttons

        self.Buttons = Buttons(parent, self.alarm_manager)
        self.parent = parent
        # Aktualisieren Sie den Zustand der "Stop" und "Snooze" Schaltflächen basierend auf dem Alarmzustand
        state = NORMAL if global_state.get_state(wecker_index) else DISABLED
        print(f"Updating button states to {state}")  # Debugging-Ausgabe
        self.buttons.button_stop_obj.config(state='state')
        self.buttons.button_snooze_obj.config(state='state')'''

    def get_current_mode(self):
        return self.change_button_text.get()

    def function_change(self):
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


class Threads:
    @staticmethod
    def start_uhrzeit(time_label):
        uhr = Uhrzeit()
        uhrzeit_thread = threading.Thread(target=uhr.uhrzeit, args=(time_label,))
        uhrzeit_thread.daemon = True
        uhrzeit_thread.start()

    @staticmethod
    def start_alarm_manager(alarm_manager):
        alarm_manager_thread = threading.Thread(target=alarm_manager.manage_alarms)
        alarm_manager_thread.daemon = True
        alarm_manager_thread.start()



class Uhrzeit:
    def __init__(self):
        self.time_label = StringVar()
        self.time_label.set('00:00:00')
        self.uhrzeit_thread = threading.Thread(target=self.uhrzeit, args=(self.time_label,))
        self.uhrzeit_thread.daemon = True

    @staticmethod
    def uhrzeit(time_label):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_label.set(current_time)
            time.sleep(1)

