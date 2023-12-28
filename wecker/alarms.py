# Alarm-Manager-Logik
from datetime import datetime
from threading import Thread


class Alarm:
    def __init__(self, alarm_index, hours, minutes):
        self.alarm_index = alarm_index
        self.hours = hours
        self.minutes = minutes

    def run(self):
        # Warte bis die Alarmzeit erreicht ist
        while datetime.now().hour != self.hours or datetime.now().minute != self.minutes:
            time.sleep(1)

        # Spiele den Alarmton ab
        # ...

        # Setze den Alarm erneut
        self.alarm_manager.schedule_alarm(self.alarm_index, self.hours, self.minutes)


class AlarmManager:
    def __init__(self):
        self.alarm_threads = []

    def schedule_alarm(self, alarm_index, hours, minutes):
        # Erstelle einen neuen Alarm-Thread
        alarm = Alarm(alarm_index, hours, minutes)

        # Starte den Alarm-Thread
        alarm_thread = Thread(target=alarm.run)
        alarm_thread.daemon = True
        alarm_thread.start()

        # Füge den Alarm-Thread zur Liste der Alarm-Threads hinzu
        self.alarm_threads.append(alarm_thread)

    def snooze_alarm(self, alarm_index):
        # Setze den Alarm für 10 Minuten zurück
        self.alarm_threads[alarm_index].hours = datetime.now().hour
        self.alarm_threads[alarm_index].minutes = datetime.now().minute - 10

    def stop_alarm(self, alarm_index):
        # Beende den Alarm-Thread
        self.alarm_threads[alarm_index].cancel()
