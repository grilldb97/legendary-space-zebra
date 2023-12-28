from threading import Thread
from ui import GUI, MyWindow
from alarms import Alarm
from queue import Queue

# Define the AlarmThread class
class AlarmThread(Thread):
    def __init__(self, alarm_id):
        super().__init__()
        self.alarm_id = alarm_id

    def run(self):
        while True:
            alarm = queue.get()
            if alarm is None:
                break

            alarm.start_alarm()

# Initialize the alarm objects
alarm_objects = [Alarm(i, i) for i in range(3)]

# Create a queue for scheduling alarms
queue = Queue()

# Create a list of threads for alarm handling
threads = [AlarmThread(i) for i in range(3)]

# Create an instance of MyWindow
my_window = MyWindow(alarm_objects, queue, threads)

def main():
    # Create the window
    my_window.create_window()

    # Start the alarm clock
    GUI.start(my_window.create_window)

if __name__ == "__main__":
    main()
