import time
from datetime import datetime
import winsound
from pygame import mixer

class AlarmSound:
    def __init__(self):
        mixer.init()

    def play_alarm(self):
        freq = 500
        for _ in range(10):
            winsound.Beep(freq, 400)
            winsound.Beep(freq + 100, 150)
            time.sleep(1)

    def play_mp3(self, mp3_path):
        mixer.music.load(mp3_path)
        mixer.music.play()

class AlarmManager:
    def __init__(self, buttons, button_functions):
        self.buttons = buttons
        self.button_functions = button_functions
        self.alarms = []
        self.alarm_sound = AlarmSound()

    def add_alarm(self, wecker_index, alarm_time, mode, mp3_path):
        self.alarms.append({'wecker_index': wecker_index, 'alarm_time': alarm_time, 'mode': mode, 'mp3_path': mp3_path})

    def run_alarms(self):
        while True:
            if self.alarms:
                current_time = datetime.now().strftime("%H:%M")
                for alarm in self.alarms:
                    print(f"Checking alarm: {alarm}")  # Debug-Ausgabe
                    alarm_time = alarm['alarm_time']
                    if alarm_time == current_time and not self.button_functions.alarm_on:
                        # Alarm auslösen
                        if alarm['mode'] == "Alarm":
                            print("Alarm")
                            self.alarm_sound.play_alarm()
                        else:
                            self.alarm_sound.play_mp3(alarm['mp3_path'])
            time.sleep(1)
