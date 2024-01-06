import queue
import time
import winsound
from pygame import mixer
from functions import Uhrzeit, global_alarm_queue_instance


class AlarmSound:
    def __init__(self):
        self.is_playing = {}
        mixer.init()

    def run_play(self, mode, mp3_path, button_stop, button_snooze, wecker_index, alarm_event):
        alarm_event['is_playing'] = True
        while alarm_event['is_playing']:
            if mode == "Alarm":
                self.play_alarm(wecker_index, alarm_event)
            else:
                self.play_mp3(mp3_path, wecker_index)
            time.sleep(1)  # Warten Sie eine Sekunde, bevor Sie erneut überprüfen, ob der Alarm gestoppt wurde

    @staticmethod
    def play_alarm(wecker_index, alarm_event):
        freq = 500
        for _ in range(10):
            if not alarm_event['is_playing']:
                break
            winsound.Beep(freq, 400)
            winsound.Beep(freq + 100, 150)
            time.sleep(1)

    @staticmethod
    def play_mp3(mp3_path, wecker_index):
        mixer.music.load(mp3_path)
        mixer.music.play()

    @staticmethod
    def stop_play(wecker_index, alarm_event):
        print(f"stop_play called for wecker_index {wecker_index}")  # Debugging-Ausgabe
        alarm_event['is_playing'] = False


class AlarmManager:
    def __init__(self, buttons, button_functions):
        self.buttons = buttons
        self.button_functions = button_functions
        self.alarms = []
        self.alarm_sound = AlarmSound()
        self.uhrzeit = Uhrzeit()
        self.uhrzeit.uhrzeit_thread.start()
        self.alarm_queue_instance = global_alarm_queue_instance


    def manage_alarms(self):
        while True:
            # Überprüfen Sie, ob die Warteschlange leer ist
            if not self.alarm_queue_instance.alarm_queue_global.empty():
                # Holen Sie das nächste alarm_event aus der Warteschlange
                alarm_event = self.alarm_queue_instance.alarm_queue_global.get()
                alarm_event['is_playing'] = True
                # Holen Sie den wecker_index aus dem alarm_event
                wecker_index = alarm_event['wecker_index']
                # Fügen Sie das alarm_event in den entsprechenden alarm_queue_tab ein
                self.buttons[wecker_index].alarm_queue_tab.put(alarm_event)


