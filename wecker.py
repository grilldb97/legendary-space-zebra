import time
from datetime import datetime
from tkinter import *
import threading
import winsound


def uhrzeit(time_label):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_label.set(current_time)
        time.sleep(1)


def alarm():
    freq = 500
    for i in range(16):
        freq -= 100
        winsound.Beep(freq, 400)
        freq += 100
        winsound.Beep(freq, 150)


def wecker(wecker_zeit):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        time.sleep(1)
        if current_time == wecker_zeit:
            alarm_thread = threading.Thread(target=alarm)
            alarm_thread.start()
            break


def set_wecker_zeit(stunden, minuten):
    stunden_value = stunden.get()
    minuten_value = minuten.get()
    if (stunden_value.isdigit() and minuten_value.isdigit() and 0 <= int(stunden_value) < 24
            and 0 <= int(minuten_value) < 60):
        wecker_zeit = stunden_value + ":" + minuten_value
        wecker_thread = threading.Thread(target=wecker, args=(wecker_zeit,))
        wecker_thread.start()
    else:
        print("Bitte geben Sie eine gültige Zeit ein.")


def create_window():
    window = Tk()
    window.title("WECKER")
    window.geometry("300x200")

    time_label = StringVar()
    time_label.set('00:00:00')

    label = Label(window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
    label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu

    uhrzeit_thread = threading.Thread(target=uhrzeit, args=(time_label,))
    uhrzeit_thread.start()

    time_frame = Frame(window)
    time_frame.grid(row=1, column=1, pady=10)  # Fügt vertikalen Abstand hinzu

    stunden = Spinbox(time_frame, from_=0, to=23, width=5)
    stunden.grid(row=0, column=0)  # Platziert in dem time_frame

    minuten = Spinbox(time_frame, from_=0, to=59, width=5)
    minuten.grid(row=0, column=1)  # Platziert in dem time_frame

    button = Button(window, text="Wecker stellen", command=lambda: set_wecker_zeit(stunden, minuten))
    button.grid(row=2, column=1, padx=5, pady=10)  # Fügt horizontalen und vertikalen Abstand hinzu

    # Leere Spalten auf beiden Seiten hinzufügen
    window.grid_columnconfigure(1, weight=1)

    window.mainloop()


if __name__ == "__main__":
    create_window()
