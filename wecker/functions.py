from tkinter import Spinbox
import time
from datetime import datetime
import threading

class SpinboxCreator:
    @staticmethod
    def create_spinbox(parent, from_, to, row, column):
        spinbox = Spinbox(parent, from_=from_, to=to, width=5)
        spinbox.grid(row=row, column=column)  # Platziert in dem time_frame
        return spinbox

class Threads:
    @staticmethod
    def start_uhrzeit(time_label):
        uhr = Uhrzeit()
        thread = threading.Thread(target=uhr.uhrzeit, args=(time_label,))
        thread.daemon = True
        thread.start()
class Alarm:
    print("")
class Uhrzeit:
    def uhrzeit(self, time_label):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time_label.set(current_time)
            time.sleep(1)
class Wecker:
    print("")