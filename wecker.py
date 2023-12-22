# Teil 1
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import threading
import winsound
from queue import Queue

snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion
alarm_on = [False, False, False]  # Zustand des Alarms für jede Weckzeit
wecker_zeit = ["", "", ""]  # Speichert die Weckzeiten
wecker_set = [False, False, False]  # Speichert, ob der Wecker eingestellt wurde
# Erstellen Sie eine globale Warteschlange
alarm_queue = Queue()


def uhrzeit(time_label):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_label.set(current_time)
        time.sleep(1)


def alarm(index):
    global alarm_on
    alarm_on[index] = True
    freq = 500
    print(f"Alarm-Funktion für Wecker {index+1} wird gestartet")
    # Fügt eine separate while-Schleife hinzu
    while alarm_on[index]:
        # Die ursprüngliche while-Schleife wird zu einer inneren Schleife
        for _ in range(10):  # Wiederholt den Alarm 10 Mal
            if not alarm_on[index]:  # Überprüft, ob der Alarm ausgeschaltet wurde
                break
            winsound.Beep(freq, 400)
            winsound.Beep(freq + 100, 150)
        time.sleep(1)  # Pausiert für 1 Sekunde zwischen den Alarmen


'''def alarm_manager():
    print("Alarm-Manager-Funktion wird gestartet")
    while True:
        # Warten Sie auf einen Index in der Warteschlange
        index = alarm_queue.get()
        # Starten Sie den Alarm-Thread
        alarm_thread = threading.Thread(target=alarm, args=(index,))
        alarm_thread.start()
        print(f"Alarm-Thread für Wecker {index+1} wurde gestartet")
        # Markieren Sie den Task als erledigt, damit die Warteschlange weiß, dass sie den nächsten Task starten kann
        alarm_queue.task_done()'''


def alarm_manager():
    while True:
        print(f"Größe der Alarm-Warteschlange: {alarm_queue.qsize()}")
        # Warten Sie auf einen Index in der Warteschlange
        index = alarm_queue.get()
        # Starten Sie den Alarm-Thread
        alarm_thread = threading.Thread(target=alarm, args=(index,))
        alarm_thread.start()
        print(f"Alarm-Thread für Wecker {index+1} wurde gestartet")


def snooze(index):
    global alarm_on
    alarm_on[index] = False
    snooze_time_in_seconds = snooze_time * 60
    time.sleep(snooze_time_in_seconds)
    if not alarm_on[index]:
        # Fügen Sie den Index zur Warteschlange hinzu, anstatt den Thread hier zu starten
        alarm_queue.put(index)


def stop_alarm(index, stunden_spinboxes, minuten_spinboxes):
    global alarm_on
    alarm_on[index] = False
    # Aktiviere die Spinboxen wieder
    stunden_spinboxes[index].config(state="normal")
    minuten_spinboxes[index].config(state="normal")


def delete_alarm(index, stunden_spinboxes, minuten_spinboxes):
    global alarm_on, wecker_set
    alarm_on[index] = False
    wecker_set[index] = False
    # Leere die Spinboxen
    stunden_spinboxes[index].delete(0, 'end')
    minuten_spinboxes[index].delete(0, 'end')
    # Aktiviere die Spinboxen wieder
    stunden_spinboxes[index].config(state="normal")
    minuten_spinboxes[index].config(state="normal")


def wecker(index):
    global alarm_on, wecker_zeit
    print(f"Wecker-Funktion für Wecker {index + 1} wird gestartet")
    while True:
        current_time = datetime.now().strftime("%H:%M")
        time.sleep(1)
        if current_time == wecker_zeit[index] and not alarm_on[index]:
            print(f"Wecker {index+1} wird zur Warteschlange hinzugefügt")
            alarm_queue.put(index)


# Teil 2
def set_wecker_zeit(stunden_spinboxes, minuten_spinboxes, index):
    global alarm_on, wecker_set, wecker_zeit

    if not wecker_set[index]:
        stunden = stunden_spinboxes[index].get()
        minuten = minuten_spinboxes[index].get()
        if (stunden.isdigit() and minuten.isdigit() and 0 <= int(stunden) < 24
                and 0 <= int(minuten) < 60):
            wecker_zeit[index] = stunden + ":" + minuten
            wecker_set[index] = True
            alarm_on[index] = True
            # Deaktiviere die Spinbox des gerade eingestellten Weckers
            stunden_spinboxes[index].config(state="disabled")
            minuten_spinboxes[index].config(state="disabled")
            # Starte den Wecker
            wecker_thread = threading.Thread(target=wecker, args=(index,), daemon=True)
            wecker_thread.start()
        else:
            print("Bitte geben Sie eine gültige Zeit ein.")
    else:
        print("Wecker ist bereits eingestellt.")


def open_help_window():
    help_window = Toplevel()
    help_window.title("Hilfe")
    Label(help_window, text="Hier sind die Anweisungen...").pack()


def create_window():
    window = Tk()
    window.title("WECKER")
    window.geometry("400x250")  # Vergrößert das Fenster
    window.resizable(False, False)  # Verhindert das Ändern der Fenstergröße
    window.attributes('-toolwindow', True)  # Blendet den Maximierungsbutton aus

    time_label = StringVar()
    time_label.set('00:00:00')

    label = Label(window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
    label.grid(row=0, column=1, pady=10)  # Fügt vertikalen Abstand hinzu

    uhrzeit_thread = threading.Thread(target=uhrzeit, args=(time_label,))
    uhrzeit_thread.start()

    # Starten Sie den Alarm-Manager in einem eigenen Thread
    alarm_manager_thread = threading.Thread(target=alarm_manager)
    alarm_manager_thread.start()

    tab_control = ttk.Notebook(window)
    tab_control.grid(row=1, column=1, pady=10, sticky='nsew')  # Fügt vertikalen Abstand hinzu

    stunden_spinboxes = [None, None, None]
    minuten_spinboxes = [None, None, None]

    for i in range(3):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=f"Wecker {i + 1}")

        time_frame = Frame(tab)  # Erstellt das time_frame im tab
        time_frame.place(relx=0.502, rely=0.1, anchor=CENTER)  # Zentriert das time_frame im tab

        stunden_spinboxes[i] = Spinbox(time_frame, from_=0, to=23, width=5)
        stunden_spinboxes[i].grid(row=0, column=0)

        minuten_spinboxes[i] = Spinbox(time_frame, from_=0, to=59, width=5)
        minuten_spinboxes[i].grid(row=0, column=1)

        button = Button(tab, text="Wecker stellen", command=lambda index=i: set_wecker_zeit(
            stunden_spinboxes, minuten_spinboxes, index))
        button.place(relx=0.400, rely=0.4, anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu

        snooze_button = Button(tab, text="Snooze/Stop", command=lambda index=i: snooze(index), bg="blue", fg="white")
        snooze_button.bind("<Double-Button-1>", lambda event, index=i: stop_alarm(
            index, stunden_spinboxes, minuten_spinboxes))
        snooze_button.place(relx=0.605, rely=0.4, anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu

        delete_button = Button(tab, text="Wecker löschen", command=lambda index=i: delete_alarm(
            index, stunden_spinboxes, minuten_spinboxes))
        delete_button.place(relx=0.502, rely=0.7, anchor=CENTER)  # Fügt horizontalen und vertikalen Abstand hinzu

    help_button = Button(window, text="?", command=open_help_window)
    help_button.place(relx=1, x=-2, y=2, anchor=NE)

    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)  # Erlaubt es dem tab_control, sich mit dem Fenster zu vergrößern

    window.mainloop()


if __name__ == "__main__":
    create_window()
