import numpy
import time
from datetime import datetime
import winsound


class AlarmSound:

    def play_alarm(self):
        freq = 500
        for _ in range(10):  # Wiederholt den Alarm 10 Mal
            winsound.Beep(freq, 400)
            winsound.Beep(freq + 100, 150)
            time.sleep(1)  # Pausiert für 1 Sekunde zwischen den Alarmen

    def play_mp3(selfself, mp3_path):
        print("musik")


class AlarmManager:
    def __init__(self):
        self.alarms = []
        self.alarm_sound = AlarmSound()  # Erstellen Sie eine Instanz von AlarmSound
        self.selected_mp3 = None  # Fügen Sie diese Zeile hinzu

    def alarm_exists(self, wecker_index):
        # Überprüfen Sie, ob ein Alarm für den gegebenen Wecker existiert
        for alarm in self.alarms:
            if alarm['wecker_index'] == wecker_index:
                return True
        return False

    def set_selected_mp3(self, mp3_path):
        self.selected_mp3 = mp3_path

    def add_alarm(self, wecker_index, stunden, minuten, mode, mp3_path):
        # Überprüfen Sie, ob bereits ein Alarm für diesen Wecker existiert
        if not self.alarm_exists(wecker_index):
            # Fügen Sie den Alarm nur hinzu, wenn noch kein Alarm für diesen Wecker existiert
            self.alarms.append({'wecker_index': wecker_index, 'stunden': stunden, 'minuten': minuten, 'mode': mode,
                                'mp3_path': mp3_path})
        else:
            print(f"Ein Alarm für Wecker {wecker_index} existiert bereits.")

    def run_alarms(self):
        while True:  # Dauerschleife, um ständig auf Alarme zu warten
            if self.alarms:  # Überprüfen Sie, ob die Liste self.alarms nicht leer ist
                current_time = datetime.now().strftime("%H:%M")
                for alarm in self.alarms:
                    alarm_time = f"{alarm['stunden']}:{alarm['minuten']}"
                    if alarm_time == current_time:
                        if alarm['mode'] == "Alarm":
                            self.alarm_sound.play_alarm()
                        else:
                            self.alarm_sound.play_mp3(alarm['mp3_path'])
            time.sleep(1)  # Pausieren Sie für eine Sekunde, bevor Sie die Schleife erneut durchlaufen
