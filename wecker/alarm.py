import queue
import time
import winsound
from pygame import mixer
from functions import Uhrzeit, global_alarm_queue_instance, ButtonFunctions


class AlarmSound:
    def __init__(self):
        self.is_playing = {}
        mixer.init()

    @staticmethod
    def play_alarm():
        freq = 500
        while True:
            winsound.Beep(freq, 400)
            winsound.Beep(freq + 100, 150)
            time.sleep(1)

    @staticmethod
    def play_mp3(mp3_path):
        mixer.music.load(mp3_path)
        mixer.music.play()




    @staticmethod
    def run_play(mode, mp3_path):
        if mode == "Alarm":
            AlarmSound.play_alarm()
        else:
            AlarmSound.play_mp3(mp3_path)


class AlarmManager:
    def __init__(self, buttons, button_functions):
        self.buttons = buttons
        self.button_functions = button_functions
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

    def stop_play(self):
        alarm_event = self.buttons.alarm_queue_tab.get()
        alarm_event['is_playing'] = True
        # Holen Sie den wecker_index aus dem alarm_event
        wecker_index = alarm_event['wecker_index']
        self.buttons[wecker_index].alarm_queue_tab.put(alarm_event)
        self.buttons[wecker_index].alarm_queue_tab.lock.acquire(alarm_event)
