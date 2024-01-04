import time
import winsound
from pygame import mixer
from functions import alarm_queue, Threads, Uhrzeit
from tkinter import *




class AlarmSound:
    def __init__(self):
        mixer.init()


    def run_play(self, mode, mp3_path, button_stop, button_snooze):
        button_stop.config(state='normal')
        button_snooze.config(state='normal')
        if mode == "Alarm":
            self.play_alarm()
        else:
            self.play_mp3(mp3_path)


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
        self.uhrzeit = Uhrzeit()
        self.uhrzeit.uhrzeit_thread.start()

    def manage_alarms(self):
        while True:
            current_time = self.uhrzeit.get_current_time()
            # Überprüfen Sie, ob ein Alarm-Event in der Warteschlange ist
            if not alarm_queue.empty():
                alarm_event = alarm_queue.get()
                while alarm_event['alarm_time'] != current_time:
                    time.sleep(1)  # Warte für eine Sekunde
                    current_time = self.uhrzeit.get_current_time()  # Aktualisiere die aktuelle Zeit
                # Wenn die Alarmzeit gleich der aktuellen Zeit ist, starten Sie den Alarm
                Threads.start_alarm(self.alarm_sound, alarm_event['mode'], alarm_event['mp3_path'])
                # Markieren Sie das Alarm-Event als erledigt
                alarm_queue.task_done()
