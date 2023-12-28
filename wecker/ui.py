# GUI des Weckers
from tkinter import *
import wecker

class MyWindow:
    def __init__(self):
        # Erstelle das Hauptfenster
        self.main_window = Tk()
        self.main_window.title("Wecker")

        # Erstelle die Tabs
        for index in range(3):
            tab = Frame(self.main_window)
            tab.grid(row=0, column=index)

        # Erstelle die Spinboxes für Stunden und Minuten
        for index, tab in enumerate(self.tabs):
            time_frame = Frame(tab)
            time_frame.place(relx=0.502, rely=0.1, anchor=CENTER)

            # Setze die Werte der Spinboxes
            stunden_spinbox = Spinbox(time_frame, from_=0, to=23)
            minuten_spinbox = Spinbox(time_frame, from_=0, to=59)

            # Binde die Spinbox-Events
            stunden_spinbox.bind("<ButtonRelease-1>", lambda event: self.set_alarm(index))
            minuten_spinbox.bind("<ButtonRelease-1>", lambda event: self.set_alarm(index))

        # Erstelle den Snooze-Button
        snooze_button = Button(self.main_window, text="Snooze", command=self.snooze)
        snooze_button.grid(row=1, column=0, columnspan=3)

        # Erstelle den Stop-Button
        stop_button = Button(self.main_window, text="Stop", command=self.stop_alarm)
        stop_button.grid(row=2, column=0, columnspan=3)

        # Erstelle den Help-Button
        help_button = Button(self.main_window, text="Hilfe", command=lambda: self.show_help())
        help_button.grid(row=3, column=0, columnspan=3)

        # Starte den Hauptloop
        self.main_window.mainloop()

    def set_alarm(self, index):
        # Rufe die entsprechende Funktion in wecker.py auf
        wecker.set_alarm(index, stunden_spinbox.get(), minuten_spinbox.get())

    def snooze(self):
        # Rufe die entsprechende Funktion in wecker.py auf
        wecker.snooze()

    def stop_alarm(self):
        # Rufe die entsprechende Funktion in wecker.py auf
        wecker.stop_alarm()

    def show_help(self):
        # Rufe die entsprechende Funktion in wecker.py auf
        wecker.show_help()
