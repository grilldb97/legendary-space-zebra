# alarm.py
class AlarmManager:
    def __init__(self):
        self.alarms = []

    def add_alarm(self, alarm_time):
        # alarm_time ist ein Tupel (stunden, minuten)
        # Fügen Sie die Weckerzeit direkt zur Liste der Alarme hinzu
        self.alarms.append(alarm_time)
        print(f"Alarm hinzugefügt: {alarm_time}")

    def run_alarms(self):
        for alarm in self.alarms:
            alarm.run()