from tkinter import *
from tkinter import ttk
from functions import SpinboxCreator
from functions import Threads


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.show_time()
        self.show_tabs()



    def show_window(self):
        self.window.title("WECKER")
        self.window.geometry("400x250")  # Vergrößert das Fenster
        self.window.resizable(False, False)  # Verhindert das Ändern der Fenstergröße
        self.window.attributes('-toolwindow', True)  # Blendet den Maximierungsbutton aus
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

    def create_time_frame(self, parent):
        time_frame = Frame(parent)  # Erstellt das time_frame im tab
        time_frame.place(relx=0.5, rely=0.1, anchor=CENTER)  # Zentriert das time_frame im tab

        SpinboxCreator.create_spinbox(time_frame, 0, 23, 0, 0)
        SpinboxCreator.create_spinbox(time_frame, 0, 59, 0, 1)


    def show_tabs(self):
        tab_control = ttk.Notebook(self.window)
        tab_control.grid(row=1, column=1, pady=10, sticky='nsew')  # Fügt vertikalen
        for i in range(3):
            self.tab = ttk.Frame(tab_control)
            tab_control.add(self.tab, text=f"Wecker {i + 1}")
            self.create_time_frame(self.tab)
            self.show_buttons()
    def show_time(self):
        time_label = StringVar()
        time_label.set('00:00:00')
        label = Label(self.window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
        label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu
        Threads.start_uhrzeit(time_label)
    def show_buttons(self):
        self.button_help()
        self.button_stop()
        self.button_snooze()
        self.button_wecker_stellen()
        self.button_delete()
        self.button_change_alarm_musik()

    def button_wecker_stellen(self):
        button_wecker_stellen = Button(self.tab, text="stellen", width=6)
        button_wecker_stellen.place(relx=0.420, rely=0.400,
                                    anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu

    def button_delete(self):
        delete_button = Button(self.tab, text="löschen", width=6)
        delete_button.place(relx=0.420, rely=0.650, anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu

    def button_snooze(self):
        button_snooze = Button(self.tab, text="Snooze")
        button_snooze.place(relx=0.500, rely=0.300)
        button_snooze.config(bg="blue", fg="white", anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu
    def button_stop(self):
        button_stop = Button(self.tab, text="Stop")
        button_stop.place(relx=0.500, rely=0.300, x=49.5)  # Plaziert den Stop-Button direkt neben dem Snooze-Button
        button_stop.config(bg="red", fg="white", anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu


    def button_change_alarm_musik(self):
        button_change_alarm_musik = Button(self.tab, text="Change", width=11)
        button_change_alarm_musik.place(relx=0.605, rely=0.650, anchor=CENTER)

    def button_help(self):
        button_help = Button(self.window, text="?")
        button_help.place(relx=1, x=-2, y=2, anchor=NE)



