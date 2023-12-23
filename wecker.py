import time
from datetime import datetime
from tkinter import *
from tkinter import filedialog
import threading
import winsound
from queue import Queue
from functools import partial
import pygame
import os
from tkinter import ttk
from tkinter import StringVar

# Erstellen Sie die StringVar-Objekte hier, nachdem das Fenster erstellt wurde
global button_labels

# Erstellen Sie eine leere Liste von Tabs am Anfang Ihres Programms
tabs = []

snooze_time = 10  # Zeit in Minuten für die Snooze-Funktion
alarm_on = [False, False, False]  # Zustand des Alarms für jede Weckzeit
wecker_zeit = ["", "", ""]  # Speichert die Weckzeiten
wecker_set = [False, False, False]  # Speichert, ob der Wecker eingestellt wurde
alarm_typ = [0, 0, 0]  # Globale Liste der Alarmtypen (0 für winsound.beep, 1 für Musik)
musik_dateien = ["nonexistent.mp3", "nonexistent.mp3", "nonexistent.mp3"]  # Globale Liste der Musikdateien


# Erstellen Sie eine globale Warteschlange
alarm_queue = Queue()

# Globale Liste der Alarm-Threads
alarm_threads = [threading.Thread(target=lambda: None) for _ in range(3)]


def uhrzeit(time_label):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_label.set(current_time)
        time.sleep(1)


def alarm_mit_beep(index):
    global alarm_on
    alarm_on[index] = True
    freq = 500
    while alarm_on[index]:
        for _ in range(10):
            if not alarm_on[index]:
                break
            winsound.Beep(freq, 400)
            winsound.Beep(freq + 100, 150)
        time.sleep(1)

def blink(tab):
    current_color = tab.cget("background")  # Holt die aktuelle Hintergrundfarbe des Tabs
    next_color = "red" if current_color == "white" else "white"
    tab.config(background=next_color)  # Ändert die Hintergrundfarbe des Tabs


def start_blinking(tab):
    current_color = tab.cget("background")
    next_color = "red" if current_color == "white" else "white"
    for _ in range(10):
        tab.config(background=next_color)
        time.sleep(1)
        next_color = "red" if next_color == "white" else "white"

def alarm(index):
    global alarm_on, wecker_zeit
    if alarm_on[index]:
        if alarm_typ[index] == 0:
            alarm_mit_beep(index)
        else:
            alarm_mit_musik(index)
        threading.Thread(target=start_blinking, args=(tabs[index], index)).start()
        alarm_queue.put(index)
        while alarm_threads[index].is_alive():
            time.sleep(0.1)
        alarm_on[index] = False
        alarm_threads[index].join()

def snooze(index):
    global alarm_on
    if wecker_set[index]:
        alarm_on[index] = False
        snooze_time_in_seconds = snooze_time * 60
        time.sleep(snooze_time_in_seconds)
        if not alarm_on[index]:
            alarm_queue.put(index)


def stop_alarm(index, stunden_spinboxes, minuten_spinboxes):
    global alarm_on
    if wecker_set[index]:
        alarm_on[index] = False
        if alarm_threads[index].is_alive():
            alarm_threads[index].join()
        delete_alarm(index, stunden_spinboxes, minuten_spinboxes)  # Löscht den Wecker
        stunden_spinboxes[index].delete(0, 'end')
        minuten_spinboxes[index].delete(0, 'end')
        stunden_spinboxes[index].insert(0, '0')
        minuten_spinboxes[index].insert(0, '0')


def delete_alarm(index, stunden_spinboxes, minuten_spinboxes):
    global alarm_on, wecker_set, alarm_typ
    if wecker_set[index]:
        alarm_on[index] = False
        wecker_set[index] = False
        stunden_spinboxes[index].delete(0, 'end')
        minuten_spinboxes[index].delete(0, 'end')
        stunden_spinboxes[index].insert(0, '0')
        minuten_spinboxes[index].insert(0, '0')
        stunden_spinboxes[index].config(state="normal")
        minuten_spinboxes[index].config(state="normal")
        button_labels[index].set("Alarm")
        alarm_typ[index] = 0


def wecker(index):
    global alarm_on, wecker_zeit
    print(f"Wecker-Funktion für Wecker {index + 1} wird gestartet")
    while True:
        current_time = datetime.now().strftime("%H:%M")
        time.sleep(1)
        if current_time == wecker_zeit[index] and not alarm_on[index]:
            print(f"Wecker {index+1} wird zur Warteschlange hinzugefügt")
            alarm_queue.put(index)


def create_spinbox(time_frame, from_, to):
    spinbox = Spinbox(time_frame, from_=from_, to=to, width=5)
    return spinbox


def create_button(tab, text, command, relx, rely):
    button = Button(tab, text=text, command=command)
    button.place(relx=relx, rely=rely, anchor=CENTER)
    return button


def is_valid_time(stunden, minuten):
    return (stunden.isdigit() and minuten.isdigit() and 0 <= int(stunden) < 24
            and 0 <= int(minuten) < 60)


def waehle_musik(index):
    musik_dateien[index] = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])


def alarm_mit_musik(index):
    global alarm_on
    alarm_on[index] = True
    pygame.mixer.init()
    if os.path.isfile(musik_dateien[index]):
        pygame.mixer.music.load(musik_dateien[index])
        while alarm_on[index]:
            pygame.mixer.music.play()
            time.sleep(1)
    else:
        # Wenn die Musikdatei nicht existiert, verwenden Sie den Standard-Alarmton
        alarm_mit_beep(index)


def wechsel_alarm_typ(index):
    global alarm_typ
    alarm_typ[index] = 1 - alarm_typ[index]
    if alarm_typ[index] == 0:
        button_labels[index].set("Alarm")
    else:
        button_labels[index].set("Musik")
        waehle_musik(index)


def set_wecker_zeit(stunden_spinboxes, minuten_spinboxes, index):
    global alarm_on, wecker_set, wecker_zeit
    if not wecker_set[index]:
        stunden = stunden_spinboxes[index].get()
        minuten = minuten_spinboxes[index].get()
        if is_valid_time(stunden, minuten):
            wecker_zeit[index] = stunden + ":" + minuten
            wecker_set[index] = True
            stunden_spinboxes[index].config(state="disabled")
            minuten_spinboxes[index].config(state="disabled")
            alarm_queue.put(index)
        else:
            print("Bitte geben Sie eine gültige Zeit ein.")
    else:
        print("Wecker ist bereits eingestellt.")


def alarm_manager():
    while True:
        index = alarm_queue.get()
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            if wecker_zeit[index] == current_time:
                break
            time.sleep(1)
        alarm_threads[index] = threading.Thread(target=alarm, args=(index,))
        alarm_threads[index].daemon = True  # Mark the thread as a daemon
        alarm_threads[index].start()
        print(f"Alarm-Thread für Wecker {index+1} wurde gestartet")
        alarm_queue.task_done()

def open_help_window():
    help_window = Toplevel()
    help_window.title("Hilfe")
    Label(help_window, text="Hier sind die Anweisungen...").pack()


def create_tab(tab_control, stunden_spinboxes, minuten_spinboxes, index):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=f"Wecker {index + 1}")
    tabs.append(tab)  # Fügen Sie den erstellten Tab zur Liste hinzu

    time_frame = Frame(tab)
    time_frame.place(relx=0.502, rely=0.1, anchor=CENTER)

    stunden_spinboxes[index] = create_spinbox(time_frame, 0, 23)
    stunden_spinboxes[index].grid(row=0, column=0)

    minuten_spinboxes[index] = create_spinbox(time_frame, 0, 59)
    minuten_spinboxes[index].grid(row=0, column=1)

    create_button(tab, "Wecker stellen", partial(
        set_wecker_zeit, stunden_spinboxes, minuten_spinboxes, index), 0.400, 0.4)

    snooze_button = create_button(tab, "Snooze", partial(snooze, index), 0.605, 0.4)
    snooze_button.config(bg="blue", fg="white")

    stop_button = create_button(tab, "Stop", partial(
        stop_alarm, index, stunden_spinboxes, minuten_spinboxes), 0.705, 0.4)
    stop_button.config(bg="red", fg="white")

    create_button(tab, "Wecker löschen", partial(
        delete_alarm, index, stunden_spinboxes, minuten_spinboxes), 0.400, 0.7)

    button = Button(tab, textvariable=button_labels[index], command=partial(wechsel_alarm_typ, index), width=10)
    button.place(relx=0.650, rely=0.7, anchor=CENTER)


def create_main_window():
    window = Tk()
    window.title("WECKER")
    window.geometry("400x250")
    window.resizable(False, False)
    window.attributes('-toolwindow', True)
    return window


def create_window():
    window = create_main_window()

    # Erstellen Sie die StringVar-Objekte hier, nachdem das Fenster erstellt wurde
    global button_labels
    button_labels = [StringVar(window, value="Alarm") for _ in range(3)]

    time_label = StringVar()
    time_label.set('00:00:00')

    label = Label(window, textvariable=time_label, font=("Helvetica", 30, "bold"), fg="green")
    label.grid(row=0, column=1, pady=10)

    uhrzeit_thread = threading.Thread(target=uhrzeit, args=(time_label,))
    uhrzeit_thread.start()

    alarm_manager_thread = threading.Thread(target=alarm_manager)
    alarm_manager_thread.start()

    tab_control = ttk.Notebook(window)
    tab_control.grid(row=1, column=1, pady=10, sticky='nsew')  # Fügt vertikalen Abstand hinzu

    stunden_spinboxes = [None, None, None]
    minuten_spinboxes = [None, None, None]

    for i in range(3):
        create_tab(tab_control, stunden_spinboxes, minuten_spinboxes, i)

    help_button = Button(window, text="?", command=open_help_window)
    help_button.place(relx=1, x=-2, y=2, anchor=NE)

    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(1, weight=1)

    window.mainloop()


if __name__ == "__main__":
    create_window()
