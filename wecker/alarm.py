import numpy
import time
from datetime import datetime, timedelta
import winsound
from pygame import mixer


class AlarmSound:
    def __init__(self, alarm_manager):
        self.alarm_manager = alarm_manager
        mixer.init()

    def should_play_alarm(self):
        return not self.alarm_manager.stop_alarm

    def play_alarm(self):
        freq = 500
        while not self.alarm_manager.stop_alarm:
            if self.should_play_alarm():  # Überprüfen Sie, ob der Alarm abgespielt werden soll
                for _ in range(10):  # Wiederholt den Alarm 10 Mal
                    winsound.Beep(freq, 400)
                    winsound.Beep(freq + 100, 150)
                    time.sleep(1)  # Pausiert für 1 Sekunde zwischen den Alarmen

    def play_mp3(self, mp3_path):
        if not self.alarm_manager.stop_alarm:  # Überprüfen Sie die stop_alarm Bedingung des AlarmManager
            if self.should_play_alarm():  # Überprüfen Sie, ob der Alarm abgespielt werden soll
                mixer.music.load(mp3_path)  # Laden Sie die MP3-Datei
                mixer.music.play()  # Spielen Sie die MP3-Datei ab


class AlarmManager:
    def __init__(self, buttons):
        self.buttons = buttons
        self.alarms = []
        self.alarm_sound = AlarmSound(self)  # Erstellen Sie eine Instanz von AlarmSound
        self.selected_mp3 = None  # Fügen Sie diese Zeile hinzu
        self.stop_alarm = False  # Fügen Sie diese Zeile hinzu
        self.alarm_triggered = False
        self.buttons = None

    def set_buttons(self, buttons):
        self.buttons = buttons

    def alarm_exists(self, wecker_index):
        # Überprüfen Sie, ob ein Alarm für den gegebenen Wecker existiert
        for alarm in self.alarms:
            if alarm['wecker_index'] == wecker_index:
                return True
        return False

    def set_selected_mp3(self, mp3_path):
        self.selected_mp3 = mp3_path

    def add_alarm(self, wecker_index, alarm_time, mode, mp3_path):
        # Überprüfen Sie, ob bereits ein Alarm für diesen Wecker existiert
        if not self.alarm_exists(wecker_index):
            # Fügen Sie den Alarm nur hinzu, wenn noch kein Alarm für diesen Wecker existiert
            self.alarms.append({'wecker_index': wecker_index, 'alarm_time': alarm_time, 'mode': mode,
                                'mp3_path': mp3_path})
        else:
            print(f"Ein Alarm für Wecker {wecker_index} existiert bereits.")

    def snooze_alarm(self, wecker_index):
        # Finden Sie den Alarm, der verschoben werden soll
        for alarm in self.alarms:
            if alarm['wecker_index'] == wecker_index:
                # Konvertieren Sie die Weckerzeit in ein datetime-Objekt
                wecker_time = datetime.strptime(f"{alarm['stunden']}:{alarm['minuten']}", "%H:%M")
                # Fügen Sie 10 Minuten zur Weckerzeit hinzu
                snooze_time = (wecker_time + timedelta(minutes=10)).time()
                # Aktualisieren Sie die Weckerzeit
                alarm['stunden'], alarm['minuten'] = snooze_time.strftime("%H:%M").split(":")
                break


    def stop_alarm(self):
        self.stop_alarm = True

    def run_alarms(self):
        while True:  # Dauerschleife, um ständig auf Alarme zu warten
            if self.alarms:  # Überprüfen Sie, ob die Liste self.alarms nicht leer ist
                current_time = datetime.now().strftime("%H:%M")
                for alarm in self.alarms:
                    alarm_time = alarm['alarm_time']
                    if alarm_time == current_time:
                        self.buttons.button_snooze(alarm['wecker_index']).config(state='normal')
                        self.buttons.button_stop().config(state='normal')
                        print(f"Running alarm for {alarm['alarm_time']}")  # Debug 4
                        if not self.stop_alarm:  # Überprüfen Sie, ob der Stopp-Button gedrückt wurde
                            if alarm['mode'] == "Alarm":
                                self.alarm_sound.play_alarm()
                            else:
                                self.alarm_sound.play_mp3(alarm['mp3_path'])
            time.sleep(1)  # Pausieren Sie für eine Sekunde, bevor Sie die Schleife erneut durchlaufen

