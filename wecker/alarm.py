import threading
import time

class Alarm:
    def __init__(self, index):
        self.index = index
        self.thread_started = False

    def set_alarm_time(self, stunden, minuten):
        # Setzen Sie die Alarmzeit basierend auf den gegebenen Stunden und Minuten
        self.alarm_time = stunden + ":" + minuten

    def start_alarm(self):
        # Implementieren Sie die Logik zum Starten des Alarms
        pass

class AlarmManager:
    def __init__(self):
        self.alarms = []

    def add_alarm(self, alarm):
        self.alarms.append(alarm)

class AlarmThreadManager:
    def __init__(self, alarm_manager):
        self.alarm_manager = alarm_manager

    def check_for_new_alarms(self):
        while True:
            # Überprüfen Sie, ob neue Alarme hinzugefügt wurden
            for alarm in self.alarm_manager.alarms:
                if not alarm.thread_started:
                    print(f"Alarm {alarm.index} vom AlarmThreadManager erkannt")
                    thread = threading.Thread(target=alarm.start_alarm)
                    thread.daemon = True
                    thread.start()
                    alarm.thread_started = True
            time.sleep(1)

class AlarmSetter:
    def __init__(self, index, stunden_spinbox, minuten_spinbox, button_functions):
        self.index = index
        self.stunden_spinbox = stunden_spinbox
        self.minuten_spinbox = minuten_spinbox
        self.button_functions = button_functions

    def command(self):
        def set_alarm():
            self.button_functions.function_stellen(self.index, self.stunden_spinbox, self.minuten_spinbox)
        thread = threading.Thread(target=set_alarm)
        thread.start()