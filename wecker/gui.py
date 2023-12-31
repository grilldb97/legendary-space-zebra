from tkinter import *
from tkinter import ttk
from functions import SpinboxCreator
from functions import Threads
from help import HelpWindow
from buttons import Buttons


class MainWindow:
    def __init__(self):
        self.help_window = HelpWindow()
        self.window = Tk()
        self.show_time()
        self.buttongui = Buttons(self.window)  # Geben Sie das Hauptfenster als Elternteil an
        self.buttongui.button_help()
        self.stunden_spinboxes = []
        self.minuten_spinboxes = []
        self.show_tabs()




    def show_window(self):
        self.window.title("WECKER")
        self.window.geometry("400x250")  # Vergrößert das Fenster
        self.window.resizable(False, False)  # Verhindert das Ändern der Fenstergröße
        self.window.attributes('-toolwindow', True)  # Blendet den Maximierungsbutton aus
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_rowconfigure(1, weight=1)


    def create_time_frame(self, parent):
        stunden_spinbox = SpinboxCreator.create_spinbox(parent, 0, 23, 0, 0)
        minuten_spinbox = SpinboxCreator.create_spinbox(parent, 0, 59, 0, 1)
        self.stunden_spinboxes.append(stunden_spinbox)
        self.minuten_spinboxes.append(minuten_spinbox)
        # Positionieren Sie die Spinboxen
        stunden_spinbox.place(relx=0.435, rely=0.1, anchor=CENTER)  # Ändern Sie die Werte von x und y entsprechend
        minuten_spinbox.place(relx=0.435, rely=0.1, x=45,
                              anchor=CENTER)  # Ändern Sie die Werte von x und y entsprechend

    def show_tabs(self):
        tab_control = ttk.Notebook(self.window)
        tab_control.grid(row=1, column=1, pady=10, sticky='nsew')  # Fügt vertikalen
        for i in range(3):
            self.tab = ttk.Frame(tab_control)
            tab_control.add(self.tab, text=f"Wecker {i + 1}")
            self.create_time_frame(self.tab)
            self.buttongui = Buttons(self.tab)  # Erstellen Sie eine neue Buttons-Instanz für jedes Tab
            self.show_buttons()

    def show_time(self):
        time_label = StringVar()
        time_label.set('00:00:00')
        label = Label(self.window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
        label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu
        Threads.start_uhrzeit(time_label)

    def show_buttons(self):
        self.buttongui.button_stop()
        self.buttongui.button_snooze()
        print(f"Anzahl der Stunden-Spinboxen: {len(self.stunden_spinboxes) + 1}")
        print(f"Anzahl der Minuten-Spinboxen: {len(self.minuten_spinboxes) + 1}")
        for i in range(len(self.stunden_spinboxes)):
            self.buttongui.button_wecker_stellen(i, self.stunden_spinboxes[i], self.minuten_spinboxes[i])
        self.buttongui.button_delete()
        self.buttongui.button_change_alarm_musik()

