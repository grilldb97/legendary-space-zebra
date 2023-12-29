# Alarm-Manager-Logik
from datetime import datetime
import threading
import logging
import pygame
logger = logging.getLogger(__name__)

class Alarm:

    def __init__(self, alarm_index, hours, minutes):
        self.validate_time(hours, minutes)
        self.alarm_index = alarm_index
        self.timer = threading.Timer(interval, self.alarm_callback)

    def validate_time(self, hours, minutes):
        if hours < 0 or hours > 23:
            raise ValueError("Hours must be 0-23")
        if minutes < 0 or minutes > 59:
            raise ValueError("Minutes must be 0-59")

    def start(self, interval):
        try:
            self.timer.start()
        except Exception as e:
            logger.error("Error starting timer: %s", e)

    def alarm_callback(self):
        # Play alarm sound
        pygame.mixer.music.load("alarm.mp3")
        pygame.mixer.music.play()

        # Reschedule the alarm
        interval = 60 * 60 # 1 hour interval
        self.start(interval)

    # Stop the current alarm sound after some time
        pygame.time.set_timer(pygame.USEREVENT, 30 * 1000) # 30 seconds

    def handle_alarm_stop(self):
        pygame.mixer.music.stop()
        # Cancel timer

class AlarmManager:
    def __init__(self):
        self._alarm_threads = []

    def get_alarm_threads(self):
        return self._alarm_threads

    def schedule_alarm(self, alarm):
        try:
            thread = threading.Thread(target=alarm.run)
            thread.start()
            self._alarm_threads.append(thread)
        except Exception as e:
            logger.error("Error scheduling alarm: %s", e)

    def snooze_alarm(self, alarm_index):
        # Setze den Alarm für 10 Minuten zurück
        self.alarm_threads[alarm_index].hours = datetime.now().hour
        self.alarm_threads[alarm_index].minutes = datetime.now().minute - 10

    def stop_alarm(self, alarm_index):
        # Beende den Alarm-Thread
        self.alarm_threads[alarm_index].cancel()
