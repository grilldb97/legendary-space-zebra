import ui
import threading
from threading import Thread
import time
from datetime import datetime
from tkinter import filedialog
import threading
import winsound
import pygame
import os
from tkinter import StringVar

snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion

# Globale Liste der Alarm-Threads
alarm_threads = [threading.Thread(target=lambda: None) for _ in range(3)]


class AlarmManager:
    def __init__(self):
        self.alarm_threads = alarm_threads

    def schedule_alarm(self, index, alarm_time):
        self.alarm_threads[index].schedule_alarm(alarm_time)

    @staticmethod
    def start_alarm_manager():
        for alarm_thread in alarm_threads:
            alarm_thread.start()


class AlarmThreadManager:
    def __init__(self):
        self.alarm_queue = threading.Queue()
        self.alarm_threads = []

    def schedule_alarm(self, index, alarm_time):
        alarm = ui.AlarmThread(index, alarm_time)
        self.alarm_threads.append(alarm)
        alarm.start()

    def start_alarm_manager(self):
        while True:
            if not self.alarm_queue.empty():
                index = self.alarm_queue.get()
                alarm = self.alarm_threads[index]
                while True:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    if alarm.alarm_time == current_time:
                        alarm.alarm_on = True
                        if alarm.alarm_typ == 0:
                            alarm.alarm_mit_beep()
                        else:
                            alarm.alarm_mit_musik()
                        threading.Thread(target=alarm.start_blinking).start()
                        break
                    time.sleep(1)
                alarm.alarm_on = False
                alarm.join()
                self.alarm_threads.remove(alarm)


class Alarm:
    def __init__(self, index, alarm_manager):
        self.index = index
        self.alarm_manager = alarm_manager

        self.alarm_on = False
        self.wecker_zeit = ""
        self.wecker_set = False
        self.alarm_typ = 0
        self.musik_dateien = "nonexistent.mp3"
        self.snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion

    def set_alarm_time(self, hours, minutes):
        if Alarm.valid_time(hours, minutes):
            self.wecker_zeit = f"{hours}:{minutes}"
            self.wecker_set = True
            self.alarm_manager.alarm_queue.put(self.index)
        else:
            print("Invalid time")

    @staticmethod
    def valid_time(hours, minutes):
        if hours < 0 or hours > 23:
            return False

        if minutes < 0 or minutes > 59:
            return False
        return True

    def snooze(self):
        if self.wecker_set:
            self.alarm_on = False
            snooze_time_in_seconds = self.snooze_time * 60
            time.sleep(snooze_time_in_seconds)
            if not self.alarm_on:
                self.alarm_manager.alarm_queue.put(self.index)

    def waehle_musik(self):
        self.musik_dateien = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])

    def alarm_mit_beep(self):
        self.alarm_on = True
        freq = 500
        while self.alarm_on:
            for _ in range(10):
                if not self.alarm_on:
                    break
                winsound.Beep(freq, 400)
                winsound.Beep(freq + 100, 150)
            time.sleep(1)

    def alarm_mit_musik(self):
        self.alarm_on = True
        pygame.mixer.init()
        if os.path.isfile(self.musik_dateien):
            pygame.mixer.music.load(self.musik_dateien)
            while self.alarm_on:
                pygame.mixer.music.play()
                time.sleep(1)
        else:
            # Wenn die Musikdatei nicht existiert, verwenden Sie den Standard-Alarmton
            self.alarm_mit_beep()

    def stop_alarm(self):
        if self.wecker_set:
            self.alarm_on = False
